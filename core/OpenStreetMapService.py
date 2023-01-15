from pathlib import Path

import osmnx as ox
import geopandas as gpd


class Map:
    def __init__(self, point, radius, layers, river, lake):
        self.shouldRenderRiver = river
        self.shouldRenderLake = lake
        print("\n##########################\n")
        print("# Query data")
        print("## Streets")
        self.streets = ox.graph_from_point(
            point,
            dist=radius,
            simplify=True,
            retain_all=False,
            truncate_by_edge=True,
            clean_periphery=True,
            custom_filter=layers
        )
        self.street_data = self.unpack_data()
        if "geometry" not in self.street_data:
            raise KeyError("geometries not found in street data!")

        if self.shouldRenderRiver is True:
            print("## Rivers")
            self.river = ox.geometries_from_point(
                point,
                dist=radius,
                tags={"water": "river"}
            )
        if self.shouldRenderLake is True:
            print("## Lakes")
            self.lake = ox.geometries_from_point(
                point,
                tags={"water": "lake"},
                dist=radius,
            )

    def unpack_data(self) -> gpd.GeoDataFrame:
        data = []
        for _, _, _, ddata in self.streets.edges(keys=True, data=True):
            data.append(ddata)
        df = gpd.GeoDataFrame(data)
        return df

    def apply_colour_palette(self):
        print(f"# Applying colour to data")

        def _map_highway_type_to_colour(row: gpd.GeoSeries) -> str:
            if isinstance(row.highway, str):
                comparer = lambda way, ref: way in ref
            else:
                comparer = lambda way, ref: any(i in ref for i in way)

            if comparer(row.highway, ["motorway"]):
                return "#0000ff"
            elif comparer(row.highway, ["trunk"]):
                return "#0000ff"
            elif comparer(
                row.highway,
                ["primary", "secondary", "tertiary", "unclassified", "residential"],
            ):
                return "#0000ff"
            else:
                return "#0000ff"

        def _map_highway_type_to_width(row: gpd.GeoSeries) -> int:
            if isinstance(row.highway, str):
                comparer = lambda way, ref: way in ref
            else:
                comparer = lambda way, ref: any(i in ref for i in way)

            if comparer(row.highway, ["motorway"]):
                return 3
            if comparer(row.highway, ["trunk"]):
                return 2
            else:
                return 1

        self.street_data["colour"] = self.street_data.apply(
            _map_highway_type_to_colour, axis=1
        )
        self.street_data["line_width"] = self.street_data.apply(
            _map_highway_type_to_width, axis=1
        )

    @property
    def streets_bbox(self):
        minx, miny, maxx, maxy = self.street_data.geometry.total_bounds
        return (maxy, miny, maxx, minx)

    def export_image(self, destination: Path):
        self.apply_colour_palette()

        print("# Generating svg")
        print("## Streets")
        generated_map, graph = ox.plot_graph(
            self.streets,
            node_size=0,
            bgcolor="#FFFFFF",
            edge_color=self.street_data["colour"].to_list(),
            edge_linewidth=1,
            edge_alpha=1,
            save=True,
            show=False,
            close=True,
            filepath=destination
        )

        if self.shouldRenderRiver is True:
            print("## Rivers")
            generated_map, graph = ox.plot_footprints(
                self.river,
                color="#0000ff",
                bbox=self.streets_bbox,
                ax=graph,
                save=True,
                show=False,
                close=True,
                filepath=destination
            )

        if self.shouldRenderLake is True:
            print("## Lakes")
            generated_map, graph = ox.plot_footprints(
                self.lake,
                color="#0000ff",
                bbox=self.streets_bbox,
                ax=graph,
                save=True,
                show=False,
                close=True,
                filepath=destination
            )

        return generated_map
