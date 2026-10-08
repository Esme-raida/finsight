export default function SummaryMetric({ label, value, isDanger }) {
    return (
        <div className="metric">
            <label>{label}</label>
            <span className={isDanger ? "danger-metric" : "safe-metric"}>{value}</span>
        </div>
    )
}