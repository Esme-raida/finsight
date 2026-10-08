export default function StatusBadge({ value }) {
    return (
        <div className="status-badge">
            <span className="live-dot"></span>
            STATUS:
            <span>{value}</span>
        </div>
    )
}