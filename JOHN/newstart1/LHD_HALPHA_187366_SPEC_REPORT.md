# LHD Halpha — Channel-Graph Closure Pilot

- Input: `Halpha-187366-1`
- Base/internal universe: top `40` channels by variance proxy
- Extended universe: all loaded channels
- Edge rule: correlation ≥ `0.8` on z-scored downsampled signals

## Results
- Base components: `37`
- Extended components: `115`
- Base components inside extended: `37`
- Mediator channels (non-base touching ≥2 base components): `0` (`LHD_HALPHA_187366_SPEC_MEDIATORS.csv`)

## Note
- This is a *fast* structural closure check (channel connectivity graph). It does not claim a full physics interpretation by itself.
