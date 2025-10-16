import React, { useState } from 'react';

const QueryInput = ({ onQuery, loading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onQuery(query.trim());
    }
  };

  return (
    <div className="query-input">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about electric vehicles or state tax data..."
            disabled={loading}
            className="query-field"
          />
          <button 
            type="submit" 
            disabled={loading || !query.trim()}
            className="query-button"
          >
            {loading ? '🔄' : '🔍'} {loading ? 'Processing...' : 'Query'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryInput;
