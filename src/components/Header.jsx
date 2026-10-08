export default function Header({ onReset }) {
    return (
        <header className="top-nav">
            <div className="brand-name">
                <span className="live-dot"></span>
                <h2>FINSIGHT</h2>
            </div>
            <div className="status-pill">
                <span className="live-pill">LIVE MODEL</span>
                <button className="reset-button" onClick={onReset} title="Reset to defaults">↺</button>
            </div>
        </header>

    )
}