import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import nearest_points


def zoneFlowPlot(flows, title, geojson_path="bidding_zones.geojson"):

   
    # MANUAL ARROW DEFINITIONS
 
    manual_arrows = [
        ("DK_2", "SE_4", 56.033782, 12.633105, "east west"),
        ("FI",   "NO_4", 68.592443, 24.842712, "north south"),
        ("NO_1", "SE_3", 60.071752, 12.474022, "east west"),
        ("SE_2", "SE_3", 61.107945, 14.840379, "north south"),
    ]

    manual_pairs = {(a, b) for a, b, *_ in manual_arrows} | {(b, a) for a, b, *_ in manual_arrows}


    # MANUAL ARROW ENDPOINTS
    def manual_arrow_endpoints(lat, lon, base_direction,
                               sender_lat, sender_lon, receiver_lat, receiver_lon,
                               OFFSET_M):

        half = OFFSET_M / 2  # 100 km each side → full 200 km

        dlat = half / 111000.0
        dlon = half / (111000.0 * np.cos(np.radians(lat)))

        base = base_direction.lower().replace("-", " ")

        if base == "east west":
            vx = dlon if receiver_lon >= sender_lon else -dlon
            vy = 0.0
        else:
            vx = 0.0
            vy = dlat if receiver_lat >= sender_lat else -dlat

        return (
            lon - vx, lat - vy,   # tail lon/lat
            lon + vx, lat + vy    # head lon/lat
        )


    # MAIN LOGIC
 
    arrow_color = "blue"
    OFFSET = 100_000  # half-length (100 km each direction)

    # -------------------------
    # Load bidding zones
    # -------------------------
    zones = gpd.read_file(geojson_path).to_crs(4326)
    zone_col = next(c for c in ("zone_name", "name", "bzn_name") if c in zones.columns)

    fix = {
        "NOS1": "NO_1", "NOS2": "NO_2", "NOM1": "NO_3", "NON1": "NO_4", "NOS5": "NO_5",
        "SE01": "SE_1", "SE02": "SE_2", "SE03": "SE_3", "SE04": "SE_4",
        "FI00": "FI", "DKE1": "DK_2", "DKW1": "DK_1",
        "NL00": "NL", "DE00": "DE_LU", "EE00": "EE", "LT00": "LT",
        "PL00": "PL", "GB00": "GB", "GBNI": "GB"
    }
    zones[zone_col] = zones[zone_col].replace(fix)
    zones = zones.dissolve(by=zone_col, as_index=True)
    zones_proj = zones.to_crs(3857)

    fig, ax = plt.subplots(figsize=(14, 16),
                           subplot_kw={"projection": ccrs.PlateCarree()})
    zones.boundary.plot(ax=ax, edgecolor="black")

    # Optional crop: remove southern Europe
    ax.set_extent([-5, 32, 54.5, 72], crs=ccrs.PlateCarree())


    # BUILD LEGEND CONTENT
   
    legend_entries = []

  
    # AUTOMATIC ARROWS
  
    for _, r in flows.iterrows():

        A, B, f = r["zoneA"], r["zoneB"], r["AC_flow_MW"]

        if np.isnan(f) or abs(f) < 1:
            continue

        # Add to legend
        legend_entries.append(f"{A} ↔ {B}: {f:.0f} MW")

        # Skip if manual arrow replaces it
        if (A, B) in manual_pairs:
            continue

        sender = A if f >= 0 else B
        receiver = B if f >= 0 else A

        polyA = zones_proj.loc[sender].geometry.buffer(0)
        polyB = zones_proj.loc[receiver].geometry.buffer(0)

        shared = polyA.intersection(polyB)
        ls = None

        if isinstance(shared, LineString):
            ls = shared
        elif isinstance(shared, MultiLineString):
            ls = max(shared.geoms, key=lambda g: g.length)

        # Fallback if no real border
        if ls is None or ls.length < 200:
            pa, pb = nearest_points(polyA, polyB)
            mid_x = (pa.x + pb.x) / 2
            mid_y = (pa.y + pb.y) / 2

            Cs = polyA.centroid
            Cr = polyB.centroid
            px, py = -(Cr.y - Cs.y), (Cr.x - Cs.x)
            px, py = px / np.hypot(px, py), py / np.hypot(px, py)
        else:
            x1, y1 = ls.coords[0]
            x2, y2 = ls.coords[-1]

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            tx, ty = x2 - x1, y2 - y1
            px, py = -ty, tx
            px, py = px / np.hypot(px, py), py / np.hypot(px, py)

        if not zones_proj.loc[receiver].geometry.contains(Point(mid_x + px * 5000, mid_y + py * 5000)):
            px, py = -px, -py

        # Arrow endpoints
        tail = Point(mid_x - px * OFFSET, mid_y - py * OFFSET)
        head = Point(mid_x + px * OFFSET, mid_y + py * OFFSET)

        pts = gpd.GeoSeries([tail, head], crs=3857).to_crs(4326)
        tlon, tlat = pts.iloc[0].x, pts.iloc[0].y
        hlon, hlat = pts.iloc[1].x, pts.iloc[1].y

        ax.annotate(
            "",
            xy=(hlon, hlat),
            xytext=(tlon, tlat),
            arrowprops=dict(arrowstyle="->", lw=2, color=arrow_color),
            transform=ccrs.PlateCarree(),
        )

    # MANUAL ARROWS
    for a, b, lat, lon, direction in manual_arrows:

        row = flows[
            ((flows["zoneA"] == a) & (flows["zoneB"] == b)) |
            ((flows["zoneA"] == b) & (flows["zoneB"] == a))
        ]
        if row.empty:
            continue

        f = row["AC_flow_MW"].values[0]
        sender, receiver = (a, b) if f >= 0 else (b, a)

        sender_cent = zones.loc[sender].geometry.centroid
        receiver_cent = zones.loc[receiver].geometry.centroid

        tlon, tlat, hlon, hlat = manual_arrow_endpoints(
            lat, lon, direction,
            sender_cent.y, sender_cent.x,
            receiver_cent.y, receiver_cent.x,
            OFFSET
        )

        ax.annotate(
            "",
            xy=(hlon, hlat),
            xytext=(tlon, tlat),
            arrowprops=dict(arrowstyle="->", lw=3, color=arrow_color),
            transform=ccrs.PlateCarree(),
        )


    # LEGEND
    legend_text = "\n".join(sorted(legend_entries))

    ax.text(
        0.02, 0.50,     # left side, centered
        legend_text,
        transform=ax.transAxes,
        fontsize=12,
        va="center",
        ha="left",
        bbox=dict(facecolor="white", alpha=0.92))

    plt.title(title)
    plt.tight_layout()
    plt.show()
    return