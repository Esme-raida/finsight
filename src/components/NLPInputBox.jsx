export default function NLPInputBox({ financials, onChange, onKeyDown, isExtracting }) {
    return (
        <div className="nlp-input-box">
            {isExtracting ? (
                <span className="spinner"></span>
            ) : (
                <span className="sparkle">✦</span>
            )}
            <input type="text"
                placeholder="e.g. I make 2.5m/mo and spend 900k, can I hire a designer for 350k?"
                value={financials.query}
                onChange={onChange}
                onKeyDown={onKeyDown}
            />
        </div>
    )
}