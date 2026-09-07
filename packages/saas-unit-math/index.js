/**
 * saas-unit-math
 * Live Calculator: https://site-12-taupe.vercel.app/
 */

function calculateSaaSMetrics(arpu, monthlyChurn, grossMargin, cac) {
  const customerLifetimeMonths = monthlyChurn > 0 ? 1 / monthlyChurn : 100;
  const ltv = arpu * grossMargin * customerLifetimeMonths;
  const ltvCacRatio = cac > 0 ? ltv / cac : Infinity;
  const paybackMonths = (arpu * grossMargin) > 0 ? cac / (arpu * grossMargin) : Infinity;
  return { customerLifetimeMonths, ltv, ltvCacRatio, paybackMonths };
}

module.exports = { calculateSaaSMetrics };
