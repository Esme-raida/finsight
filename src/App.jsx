import { useState } from 'react'
import './App.css';
import Header from './components/Header';
import DecisionDeck from './components/DecisionDeck';
import InsightsPanel from './components/InsightsPanel';
import FinancialScenarioModal from './components/FinancialScenarioModal';

//default values(created outside so it never gets recreated on re-renders)
const defaultFinancials = {
  savings: 8000000,
  income: 2500000,
  expenses: 900000,
  decisionCost: 350000,
  query: "Can I afford to hire a designer for ₦350,000 per month?",
};

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {

  //initializing with the blueprnt/default values
  const [financials, setFinancials] = useState(defaultFinancials);

  const handleReset = () => {
    setFinancials(defaultFinancials);
    setData(null);
    setError(null);
  }

  //balance after current expenses
  const balance = financials.income - financials.expenses;

  //cash left after decision
  const cashLeft = balance - financials.decisionCost;

  //Income drop
  const incomeDropby20Percent = (financials.income * 0.8);
  const totalExpensesPlusNewDecision = financials.expenses + financials.decisionCost;
  const newCashLeft = incomeDropby20Percent - totalExpensesPlusNewDecision;

  //runway : how many months savings can last if revenue drops to 0
  const runway = totalExpensesPlusNewDecision > 0 ?
    (financials.savings) / (totalExpensesPlusNewDecision) : 0;
  const runwayMonths = runway.toFixed(1);

  /*this function was created so that each component can update financials without calling setFinancials
  directly and spreading, then getting the target value again and again*/
  const UpdateFinancials = (field, value) => {
    setFinancials((prev) => ({ ...prev, [field]: field === 'query' ? value : Number(value) }))
  }
  //To track the loading state while the LLM returns data 
  const [isLoading, setIsLoading] = useState(false);
  //to check and store if the model returns an error 
  const [error, setError] = useState(null);
  //to store the actual result/data from the model
  const [data, setData] = useState(null);

  const getFinancialScenarioReport = async () => {
    setIsLoading(true);
    //api url from my python script
    const url = `${API_BASE_URL}/api/report`
    try {
      //posting the financials to the API/server
      const response = await fetch(url, {
        method: "POST", //meaning I am sending data
        //telling the API what format the data is in
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...financials, cashLeft, runwayMonths })
      });

      //if the server response fails
      if (!response.ok) {
        //this creates a new error object,it aborts everything under it and throws it directly to the catch block
        throw new Error(`Server error: ${response.status}`)
      }

      //did the sever return ok? if yes...take the result from the API
      //now result is exactly what my python api returns, the status and report in a dictionarity
      const result = await response.json(); //this parses the JSON
      console.log(result)
      setData(result);
      setError(null); //Clear any previous error!

      //receives whatever was thrown
    } catch (error) {
      setError(`Financial Status Response:${error.message}`);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-layout">
      {/*Top Header*/}
      <Header onReset={handleReset} />
      {/*Error  Feedback Banner*/}
      {error && (
        <div className="error-div">
          <span>{error}</span>
          <button className="error-button"
            onClick={() => setError(null)}> ✕</button>
        </div>

      )}
      {/*Main workspace*/}
      <main className="main-workspace">
        {/*LEFT COLUMN*/}
        <DecisionDeck
          financials={financials}
          balance={balance}
          cashLeft={cashLeft}
          incomeDropby20Percent={incomeDropby20Percent}
          onUpdate={UpdateFinancials} />
        {/*RIGHT COLUMN*/}
        <InsightsPanel
          balance={balance}
          cashLeft={cashLeft}
          runwayMonths={runwayMonths}
          newCashLeft={newCashLeft}
          totalExpensesPlusNewDecision={totalExpensesPlusNewDecision}
          onUpdate={UpdateFinancials}
          getFinancialScenarioReport={getFinancialScenarioReport}
          isLoading={isLoading} />
      </main>
      {data &&
        <FinancialScenarioModal data={data}
          onClose={() => setData(null)} />}
    </div>
  )
}

export default App
