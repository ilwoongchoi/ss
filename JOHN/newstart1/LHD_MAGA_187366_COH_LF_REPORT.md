# LHD Halpha — Channel-Graph Closure Pilot

- Input: `Magnetics_A-187366-1`
- Base/internal universe: top `40` channels by variance proxy
- Extended universe: all loaded channels
- Edge rule: correlation ≥ `0.8` on z-scored downsampled signals

## Results
- Base components: `25`
- Extended components: `41`
- Base components inside extended: `25`
- Mediator channels (non-base touching ≥2 base components): `0` (`LHD_MAGA_187366_COH_LF_MEDIATORS.csv`)

## Note
- This is a *fast* structural closure check (channel connectivity graph). It does not claim a full physics interpretation by itself.
