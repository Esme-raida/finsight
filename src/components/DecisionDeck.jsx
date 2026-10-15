import { useState } from "react";
import Slider from "./Sliders";
import SummaryMetric from "./SummaryMetric";
import NLPInputBox from "./NLPInputBox";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function DecisionDeck({ financials, balance, cashLeft, incomeDropby20Percent, onUpdate }) {


    const [isExtracting, setIsExtracting] = useState(false);
    const [feedback, setFeedback] = useState(null);

    const handleExtractAI = async () => {
        setIsExtracting(true); //turn on the loading spinner
        try {
            //send the data typed by the user to python
            const response = await fetch(`${API_BASE_URL}/api/extract`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: financials.query })
            });

            if (!response.ok) {
                throw new Error(`Extraction failed with status: ${response.status}`)
            }
            //receiving and unpacking lines from python
            const result = await response.json();
            const data = result.data;

            //Check if any financial numbers were actually detected
            const hasUpdates = (
                data.income !== null ||
                data.expenses !== null ||
                data.savings !== null ||
                data.decisionCost !== null
            );

            //If python found a number, update the slider....
            if (data.income !== null) onUpdate('income', data.income);
            if (data.expenses !== null) onUpdate('expenses', data.expenses);
            if (data.savings !== null) onUpdate('savings', data.savings);
            if (data.decisionCost !== null) onUpdate('decisionCost', data.decisionCost);
            if (data.decisionTitle !== null) onUpdate('query', data.decisionTitle);

            if (hasUpdates) {
                setFeedback({
                    type: "success",
                    title: "Numbers updated!",
                    message: "Review your sliders below, tweak any values, and click Generate Financial Scenario Report for your CFO briefing."
                });
            } else {
                setFeedback({
                    type: "info",
                    title: "No numbers detected in your question",
                    message: "We couldn't spot any amounts in that text. Try including figures (e.g. 'I make 2m/mo, can I rent for 400k?') or adjust the sliders manually below!"
                });
            }
        } catch (error) {
            console.error("Extraction failed", error);
            setFeedback({
                type: "info",
                title: "Extraction offline",
                message: "Could not connect to the extraction service. You can adjust the sliders manually below."
            });
        } finally {
            setIsExtracting(false); //turn off the loading spinner when done
        }
    };

    //To check when the user presses the Enter key on the input
    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !isExtracting) {
            handleExtractAI();
        }
    };
    return (
        <section>
            <span className="decision-workspace">DECISION &nbsp; WORKSPACE</span>
            <h1 className="welcome-title">Hello! What
                <span className="financial-decision">&nbsp; financial decision </span>
                do you want <span>to test today?</span>
            </h1>

            {/* How It Works Micro-Steps */}
            <div className="workflow-steps">
                <span className="workflow-label">HOW IT WORKS</span>
                <div className="step-tag"><span className="step-circle">1</span> Ask / Type Plan</div>
                <span className="step-arrow">→</span>
                <div className="step-tag"><span className="step-circle">2</span> Fine-tune Sliders</div>
                <span className="step-arrow">→</span>
                <div className="step-tag"><span className="step-circle">3</span> Get financial report</div>
            </div>

            {/*NLP Input box */}
            <NLPInputBox
                financials={financials}
                onChange={(e) => {
                    onUpdate('query', e.target.value);
                    if (feedback) setFeedback(null);
                }}
                onKeyDown={handleKeyDown}
                isExtracting={isExtracting}
            />
            {feedback && (
                <div className={`scenario-feedback-pill ${feedback.type}`}>
                    <div className="feedback-content">
                        <h3><strong>
                            <span>✦ &nbsp; </span>{feedback.title}</strong></h3>
                        <p>{feedback.message}</p>
                    </div>
                    <button className="feedback-dismiss-btn" onClick={() => setFeedback(null)}>✕</button>
                </div>
            )}
            <div className="quick-prompt">
                <button
                    className="glass-card quick-prompt-btn-1"
                    onClick={() => {
                        onUpdate("query", "Can I afford to hire a designer for ₦350,000 per month?");
                        onUpdate("decisionCost", 350000);
                    }}>Can I hire a designer?
                </button>
                <button
                    className="glass-card quick-prompt-btn-2"
                    onClick={() => {
                        onUpdate("query", "What if sales drop by 20%");
                        onUpdate("income", (incomeDropby20Percent))
                    }}>What if sales drop 20%?
                </button>
                <button
                    className="glass-card quick-prompt-btn-3"
                    onClick={() => {
                        onUpdate("query", "Dedicated desk at a co-working hub in Wuse 2 for ₦250,000/month");
                        onUpdate("decisionCost", 250000)
                    }}>Co-working desk in Wuse 2?</button>
            </div>

            {/*Sliders*/}
            <div className="sliders">
                {/*CURRENT SAVINGS*/}
                <div className="slider-1">
                    <Slider
                        label="CURRENT SAVINGS"
                        displayValue={`₦${financials.savings.toLocaleString()}`}
                        min="0"
                        max={Math.max(30000000, Number(financials.savings))}
                        step="50000"
                        value={financials.savings}
                        onChange={(e) => onUpdate('savings', e.target.value)}
                    />
                </div>

                {/*MONTHLY INCOME*/}
                <div className="slider-2">
                    <Slider
                        label="MONTHLY INCOME"
                        displayValue={`₦${financials.income.toLocaleString()}`}
                        min="0"
                        max={Math.max(10000000, Number(financials.income))}
                        step="25000"
                        value={financials.income}
                        onChange={(e) => onUpdate('income', e.target.value)}
                    />
                </div>

                {/*MONTHLY EXPENSES*/}
                <div className="slider-3">
                    <Slider
                        label="MONTHLY EXPENSES"
                        displayValue={`₦${financials.expenses.toLocaleString()}`}
                        min="0"
                        max={Math.max(5000000, Number(financials.expenses))}
                        step="10000"
                        value={financials.expenses}
                        onChange={(e) => onUpdate('expenses', e.target.value)}
                    />
                </div>

                {/*DECISION'S MONTHLY COST*/}
                <div className="slider-4">
                    <Slider
                        label="DECISION'S MONTHLY COST"
                        displayValue={`₦${financials.decisionCost.toLocaleString()}`}
                        min="0"
                        max={Math.max(5000000, Number(financials.decisionCost))}
                        step="50000"
                        value={financials.decisionCost}
                        onChange={(e) => onUpdate('decisionCost', e.target.value)}
                    />
                </div>

            </div>

            {/*Summary Metrics*/}
            <div className="summary-metrics">
                {/*CURRENT SURPLUS*/}
                <SummaryMetric
                    label="BALANCE AFTER CURRENT EXPENSES"
                    value={`₦${balance.toLocaleString()}`}
                    isDanger={balance < 0 ? true : false}
                />

                {/*AFTER DECISION*/}
                <SummaryMetric
                    label="CASH LEFT AFTER DECISION"
                    value={`₦${cashLeft.toLocaleString()}`}
                    isDanger={cashLeft < 0}
                />

                {/*MONTHLY IMPACT*/}
                <SummaryMetric
                    label="MONTHLY DECISION'S COST"
                    value={`₦${financials.decisionCost.toLocaleString()}`}
                    isDanger={false}
                />
            </div>
        </section>
    )
}