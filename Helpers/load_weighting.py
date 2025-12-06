"""
#Actual working weighting
def load_weight(n, snapshot_number = 17):
    snapshot = n.snapshots[snapshot_number]

    # Load per bus
    bus_load = n.loads_t.p_set.loc[snapshot].fillna(0.0)

    # Zone per bus
    bus_zone = n.loads["zone"].astype(str)

    # Total zone load
    zone_total = bus_load.groupby(bus_zone).sum()

    # Share for each bus
    bus_load_share = bus_load / zone_total[bus_zone].to_numpy()

    # Add share as new column in n.buses
    n.buses["load_share"] = bus_load_share.reindex(n.buses.index).fillna(0.0)

    return n
"""


import numpy as np

def load_weight(n, snapshot_number=17, alpha=1.75):
    snapshot = n.snapshots[snapshot_number]

    # Load per bus
    bus_load = n.loads_t.p_set.loc[snapshot].fillna(0.0)
    bus_zone = n.loads["zone"].astype(str)

    # Total load per zone
    zone_total = bus_load.groupby(bus_zone).sum()

    # Relative load in zone
    rel_load = bus_load / zone_total[bus_zone].to_numpy()

    # OVer proportional weighting: alpha > 1. Could also be = 1 to have true proportionality
    bus_weight_raw = rel_load ** alpha

    # Normalizing within each zone. Needs to add up to 1 so we dont get more load than what ENTSO says. 
    bus_weight = bus_weight_raw.groupby(bus_zone).transform(
        lambda x: x / x.sum() if x.sum() != 0 else x
    )

    # Add new column to bus for load share. 
    n.buses["load_share"] = bus_weight.reindex(n.buses.index).fillna(0.0)

    return n
