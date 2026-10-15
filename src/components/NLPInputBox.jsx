export default function NLPInputBox({ financials, onChange, onKeyDown, isExtracting, onExtract }) {
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!isExtracting && onExtract) {
            onExtract();
        }
    };

    return (
        <form className="nlp-input-box" onSubmit={handleSubmit}>
            <span className="sparkle" aria-hidden="true">✦</span>
            <input
                type="text"
                placeholder="e.g. I make 2.5m/mo and spend 900k, can I hire a designer for 350k?"
                value={financials.query}
                onChange={onChange}
                onKeyDown={onKeyDown}
                aria-label="Financial scenario question"
            />
            <button
                type="submit"
                className="extract-action-btn"
                disabled={isExtracting || !financials.query?.trim()}
                aria-label="Extract financial numbers"
            >
                {isExtracting ? (
                    <span className="spinner"></span>
                ) : (
                    <span>Analyze</span>
                )}
            </button>
        </form>
    );
}