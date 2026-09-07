/**
 * options-greeks-math
 * Live Interactive Web App: https://site-19-nine.vercel.app/
 */

function cdf(x) {
  const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741, a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
  const sign = x < 0 ? -1 : 1;
  const absX = Math.abs(x) / Math.SQRT2;
  const t = 1.0 / (1.0 + p * absX);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-absX * absX);
  return 0.5 * (1.0 + sign * y);
}

function pdf(x) {
  return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
}

function calculateGreeks(S, K, T, r, sigma) {
  const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
  const d2 = d1 - sigma * Math.sqrt(T);
  const callPrice = S * cdf(d1) - K * Math.exp(-r * T) * cdf(d2);
  const putPrice = K * Math.exp(-r * T) * cdf(-d2) - S * cdf(-d1);
  const deltaCall = cdf(d1);
  const gamma = pdf(d1) / (S * sigma * Math.sqrt(T));
  const vega = (S * pdf(d1) * Math.sqrt(T)) / 100.0;
  return { callPrice, putPrice, deltaCall, gamma, vega };
}

module.exports = { calculateGreeks };
