export default function Header({ onReset }) {
    return (
        <header className="top-nav">
            <div className="brand-name">
                <span className="live-dot"></span>
                <h2>FINSIGHT</h2>
            </div>
            <div className="status-pill">
                <span className="history-btn" onClick={onOpenHistory}>
                    📜 History {historyCount > 0 &&
                        <span className="history-badge">
                            {historyCount}
                        </span>}
                </span>
                <button className="reset-button" onClick={onReset} title="Reset to defaults">↺</button>
            </div>
        </header>

    )
}