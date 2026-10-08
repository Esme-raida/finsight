export default function NLPInputBox({ financials, onChange, onKeyDown, isExtracting }) {
    return (
        <div className="nlp-input-box">
            {isExtracting ? (
                <span className="spinner"></span>
            ) : (
                <span className="sparkle">✦</span>
            )}
            <input type="text"
                placeholder="Ask anything e.g Can I buy a new equipment?"
                value={financials.query}
                onChange={onChange}
                onKeyDown={onKeyDown}

            />
        </div>
    )
}