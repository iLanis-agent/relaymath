# Relay Math

Race pace arithmetic. Your watch says pace, the finish line says time, and somebody has to do the multiplying.

## What it computes

- **The pace truth** - finish time and distance to pace per km and per mile: 10 km in 52:30 is 5:15 per km, 8:27 per mile.
- **The finish truth** - pace and distance to finish time: a 5:15 per km pace over 10 km finishes in 52:30.
- **The relay truth** - legs added up, slowest against fastest: 4 legs: 12:10 + 11:45 + 13:02 + 12:30 = 49:27.

## Boundary

Arithmetic only. Relay Math turns the numbers you type into paces and totals; it never says what to run, how to train, or whether you are ready for a race.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, in whole seconds.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (16 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/relaymath/
Repo: https://github.com/iLanis-agent/relaymath
