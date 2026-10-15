export default function FinancialScenarioModal({ data, onClose }) {

    const report = data.report;

    //Helper for verdict styling
    const getVerdictClass = (verdict) => {
        if (verdict === "SAFE TO PROCEED") return "verdict-safe";
        if (verdict === "PROCEED WITH CAUTION") return "verdict-caution";
        return "verdict-critical";
    };

    return (
        <>
            <div className="backdrop-overlay" onClick={onClose}></div>
            <div className="modal-container glass-card" role="dialog" aria-modal="true">
                <header className="modal-header">
                    <div>
                        <span className="decision-workspace">FRACTIONAL CFO BRIEFING</span>
                        <h1 style={{ marginTop: "4px" }}>Decision Analysis</h1>
                    </div>
                    <button className="close-button" onClick={onClose}>✕</button>
                </header>

                <div className="cfo-briefing-body">
                    {/* Dynamic Verdict Badge */}
                    <div className="briefing-verdict-section">
                        <span className={`briefing-pill ${getVerdictClass(report.verdict)}`}>
                            {report.verdict}
                        </span>
                        <p className="briefing-summary">{report.bottom_line_summary}</p>
                    </div>
                    {/* Worst-Case Check */}
                    <div className="briefing-card worst-case-card">
                        <h3> ✦ 60-Day Cashflow Lag Stress Test</h3>
                        <p>{report.worst_case_analysis}</p>
                    </div>
                    {/* Actionable Checklist */}
                    <div className="briefing-card recommendations-card">
                        <h3> ✦ Tactical Mitigation Steps</h3>
                        <ul className="tactical-list">
                            {report.tactical_recommendations.map((step, index) => (
                                <li key={index} className="tactical-item">
                                    <span className="step-num">{index + 1}</span>
                                    <span>{step}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <footer className="modal-footer">
                    <button onClick={onClose} className="primary-action-btn">Got it, thanks!</button>
                </footer>
            </div>
        </>
    );
}
