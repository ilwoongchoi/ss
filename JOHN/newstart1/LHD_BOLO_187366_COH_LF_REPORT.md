# LHD Halpha — Channel-Graph Closure Pilot

- Input: `Bolometer-187366-1`
- Base/internal universe: top `40` channels by variance proxy
- Extended universe: all loaded channels
- Edge rule: correlation ≥ `0.8` on z-scored downsampled signals

## Results
- Base components: `8`
- Extended components: `10`
- Base components inside extended: `5`
- Mediator channels (non-base touching ≥2 base components): `3` (`LHD_BOLO_187366_COH_LF_MEDIATORS.csv`)

## Note
- This is a *fast* structural closure check (channel connectivity graph). It does not claim a full physics interpretation by itself.
