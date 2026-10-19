/**
 * Formats numbers into clean Naira currency strings with proper sign placement.
 * Ensures negative values display as `-₦350,000` rather than `₦-350,000`.
 */
export const formatNaira = (amt) => {
    if (amt === undefined || amt === null || isNaN(amt)) return "₦0";
    const absoluteValue = Math.abs(Math.round(amt)).toLocaleString();
    return amt < 0 ? `-₦${absoluteValue}` : `₦${absoluteValue}`;
};
