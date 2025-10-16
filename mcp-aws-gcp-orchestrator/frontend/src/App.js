import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import QueryResults from './components/QueryResults';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Received data:', data);
      setResults(data);
    } catch (err) {
      if (err.message.includes('Proxy error') || err.message.includes('Unexpected token')) {
        try {
          const response = await fetch('http://localhost:8000/api/query', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
          });
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          const data = await response.json();
          console.log('Direct API data:', data);
          setResults(data);
        } catch (directErr) {
          setError('Backend not available. Please ensure the backend server is running on port 8000.');
        }
      } else {
        setError('Network error: ' + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 MCP Orchestrator</h1>
        <p>Ask questions about electric vehicles or state tax data</p>
      </header>
      
      <main className="App-main">
        <QueryInput onQuery={handleQuery} loading={loading} />
        
        <div className="recommended-queries">
          <h3>💡 Try these example queries:</h3>
          <div className="query-examples">
            <div className="query-category">
              <h4>🚗 Electric Vehicle Data (BigQuery)</h4>
              <button onClick={() => handleQuery("What Tesla models are available?")}>What Tesla models are available?</button>
              <button onClick={() => handleQuery("Show me electric vehicles with range over 300 miles")}>Show me electric vehicles with range over 300 miles</button>
              <button onClick={() => handleQuery("What's the average MSRP of electric vehicles?")}>What's the average MSRP of electric vehicles?</button>
            </div>
            <div className="query-category">
              <h4>💰 State Tax Data (S3 Tables)</h4>
              <button onClick={() => handleQuery("What is California's tax rate?")}>What is California's tax rate?</button>
              <button onClick={() => handleQuery("Show me Texas tax information")}>Show me Texas tax information</button>
              <button onClick={() => handleQuery("Compare Colorado tax rates")}>Compare Colorado tax rates</button>
            </div>
          </div>
        </div>
        
        {error && <div className="error">{error}</div>}
        {results && (
          <div>
            <QueryResults results={results} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
