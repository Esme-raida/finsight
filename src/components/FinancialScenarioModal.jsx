import ReactMarkdown from "react-markdown"

export default function FinancialScenarioModal({ data, onClose }) {
    return (
        <>
            <div className="backdrop-overlay"></div>
            <div className="modal-container glass-card">
                <header className="modal-header">
                    <h1>AI SCENARIO BRIEFING</h1>
                    <button className="close-button" onClick={onClose}>✕</button>
                </header>

                <div className="ai-report-text">
                    <ReactMarkdown>
                        {data.report}
                    </ReactMarkdown>
                </div>
                <footer>
                    <button onClick={onClose} className="">Got it, thanks!</button>
                </footer>
            </div>
        </>
    )
}