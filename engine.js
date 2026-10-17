// Relay Math engine - race pace arithmetic in whole seconds.
// Mirrored by oracle.py; keep the op order identical.

var KM_PER_MILE = 1.609344;

function _pos(x, msg) {
  if (!isFinite(x) || x <= 0) throw new Error(msg);
  return x;
}

function _nonneg(x, msg) {
  if (!isFinite(x) || x < 0) throw new Error(msg);
  return x;
}

function _p2(n) {
  return (n < 10 ? "0" : "") + n;
}

// m:ss under an hour, h:mm:ss from an hour up.
function _clock(s) {
  var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), r = s % 60;
  if (h > 0) return h + ":" + _p2(m) + ":" + _p2(r);
  return m + ":" + _p2(r);
}

function _km(x) {
  return x % 1 === 0 ? String(x) : String(x);
}

// The pace truth: finish time and distance to pace.
function paceTruth(distanceKm, minutes, seconds) {
  _pos(distanceKm, "distance must be more than 0 km");
  _nonneg(minutes, "minutes must be 0 or more");
  _nonneg(seconds, "seconds must be 0 or more");
  var total = Math.floor(minutes * 60 + seconds + 0.5);
  if (total <= 0) throw new Error("enter a finish time over 0");
  var perKm = Math.floor(total / distanceKm + 0.5);
  var perMile = Math.floor(total / (distanceKm / KM_PER_MILE) + 0.5);
  return _km(distanceKm) + " km in " + _clock(total) + " is " + _clock(perKm) + " per km, " +
    _clock(perMile) + " per mile.";
}

// The finish truth: pace per km and distance to finish time.
function finishTruth(distanceKm, paceMin, paceSec) {
  _pos(distanceKm, "distance must be more than 0 km");
  _nonneg(paceMin, "minutes must be 0 or more");
  _nonneg(paceSec, "seconds must be 0 or more");
  var pace = Math.floor(paceMin * 60 + paceSec + 0.5);
  if (pace <= 0) throw new Error("enter a pace over 0");
  var total = Math.floor(pace * distanceKm + 0.5);
  return "A " + _clock(pace) + " per km pace over " + _km(distanceKm) + " km finishes in " + _clock(total) + ".";
}

// The relay truth: legs added up, slowest against fastest.
function relayTruth(legs) {
  if (legs.length < 2) throw new Error("a relay needs at least 2 legs");
  var secs = [];
  for (var i = 0; i < legs.length; i++) {
    var m = /^(\d{1,3}):([0-5]\d)$/.exec(String(legs[i]).trim());
    if (!m) throw new Error("leg " + (i + 1) + " must look like 12:10");
    var s = +m[1] * 60 + +m[2];
    if (s === 0) throw new Error("leg " + (i + 1) + " must be over 0:00");
    secs.push(s);
  }
  var total = 0, lo = secs[0], hi = secs[0];
  for (var j = 0; j < secs.length; j++) {
    total += secs[j];
    if (secs[j] < lo) lo = secs[j];
    if (secs[j] > hi) hi = secs[j];
  }
  var head = secs.length + " legs: " + legs.map(function (x) { return _clock(
    +/^(\d+):/.exec(String(x).trim())[1] * 60 + +/:(\d+)$/.exec(String(x).trim())[1]); }).join(" + ") +
    " = " + _clock(total);
  if (hi === lo) return head + " - every leg the same.";
  return head + " - slowest " + _clock(hi) + ", fastest " + _clock(lo) + ", a gap of " + _clock(hi - lo) + ".";
}
