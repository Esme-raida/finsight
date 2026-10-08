import StatusBadge from "./StatusBadge.jsx";
import Bullet from "./Bullets.jsx";
import MetricCard from "./MetricCard.jsx";

export default function InsightsPanel({ cashLeft, runwayMonths, newCashLeft, totalExpensesPlusNewDecision,
    onUpdate, getFinancialScenarioReport, isLoading }) {


    return (
        <aside className="insights-panel">
            <div className="aside-card glass-card">
                {/*Status badge*/}
                <StatusBadge value={cashLeft > 0 ? "SAFE TO PROCEED" : "HIGH RISK - RECONSIDER"} />
                <h1>{runwayMonths}</h1>
                <span>Months before money runs out (Runway)</span>
                <div className="runway-meter">
                    <div className="runway-fill" style={{ width: `${Math.min((runwayMonths / 36) * 100, 100)}%` }}>
                    </div>
                </div>
                <div className="runway-labels">
                    <span>0</span>
                    <span>18 month buffer</span>
                    <span>36+ months</span>
                </div>
                <ul className="bullets">
                    <Bullet
                        strongValue="Can you afford it?"
                        strongSpan={cashLeft > 0 ? `The commitment leaves ₦${cashLeft.toLocaleString()} available each month.` : `The commitment exceeds your monthly available cash`}
                    />
                    <Bullet
                        strongValue="Maintain a buffer"
                        strongSpan={`Your reserves cover ${runwayMonths} months of this commitment before additional income.`}
                    />
                    <Bullet
                        strongValue="What if things get tough?"
                        strongSpan={`With a 20% drop in your income, it would leave ₦${newCashLeft.toLocaleString()} per month after the decision.`}
                    />
                </ul>
                <button onClick={getFinancialScenarioReport} disabled={isLoading}>
                    {isLoading ? (
                        <span className="btn-loading-state">
                            <span className="spinner"></span>
                            Analyzing scenario...
                        </span>
                    ) : (
                        "Generate Financial Scenario Report"
                    )}
                </button>
            </div>
            <div className="metrics">
                <MetricCard
                    metricLabel="MINIMUM INCOME NEEDED"
                    metricValue={"₦" + totalExpensesPlusNewDecision.toLocaleString()}
                />

                <MetricCard
                    metricLabel="RISK LEVEL"
                    metricValue={cashLeft > 0 ? "LOW" : "HIGH"}
                />
            </div>
        </aside>
    )
}