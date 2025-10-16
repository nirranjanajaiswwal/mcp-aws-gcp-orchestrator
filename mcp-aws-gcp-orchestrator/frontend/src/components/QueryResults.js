import React from 'react';

const QueryResults = ({ results }) => {
  console.log('QueryResults received:', results);
  console.log('Data array:', results.data);
  console.log('Data[0]:', results.data?.[0]);
  const { status, source, data, confidence, error } = results;

  const getSourceIcon = (source) => {
    switch (source) {
      case 'gcp_bigquery':
        return '🔵 BigQuery (EV Data)';
      case 'aws_s3_tables':
        return '🟠 S3 Tables (Tax Data)';
      case 'multi_source':
        return '🔵🟠 Multi-Source (Both)';
      default:
        return '📊 Data Source';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#F44336';
  };

  if (status === 'error') {
    return (
      <div className="results error-result">
        <h3>❌ Query Error</h3>
        <p>{error}</p>
        <div className="source-info">
          <span>Attempted source: {getSourceIcon(source)}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="routing-info" style={{backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', marginBottom: '20px'}}>
        <h3>🎯 Query Routing</h3>
        <div style={{display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '10px'}}>
          <span><strong>Query:</strong> "{results.query || 'N/A'}"</span>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '10px'}}>
          <span><strong>Routed to:</strong> {getSourceIcon(source)}</span>
          <span><strong>Confidence:</strong> 
            <span style={{color: getConfidenceColor(confidence), fontWeight: 'bold', marginLeft: '5px'}}>
              {(confidence * 100).toFixed(1)}%
            </span>
          </span>
        </div>
        {results.reason && (
          <div style={{fontSize: '14px', color: '#666', fontStyle: 'italic'}}>
            <strong>Reason:</strong> {results.reason}
          </div>
        )}
      </div>
      
      <div className="query-results">
        <h3>✅ Query Results</h3>
        {source === 'multi_source' && data ? (
          <div>
            {data.tax_data && data.tax_data.length > 0 && (
              <div style={{marginBottom: '30px'}}>
                <h4>🟠 Tax Data (S3 Tables)</h4>
                <div style={{overflowX: 'auto'}}>
                  <table style={{width: '100%', borderCollapse: 'collapse', marginTop: '10px'}}>
                    <thead>
                      <tr style={{backgroundColor: '#f5f5f5'}}>
                        {Object.keys(data.tax_data[0]).map(key => (
                          <th key={key} style={{border: '1px solid #ddd', padding: '12px', textAlign: 'left'}}>
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {data.tax_data.map((row, index) => (
                        <tr key={index}>
                          {Object.values(row).map((value, i) => (
                            <td key={i} style={{border: '1px solid #ddd', padding: '12px'}}>
                              {String(value)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
            {data.ev_data && data.ev_data.length > 0 && (
              <div>
                <h4>🔵 EV Data (BigQuery)</h4>
                <div style={{overflowX: 'auto'}}>
                  <table style={{width: '100%', borderCollapse: 'collapse', marginTop: '10px'}}>
                    <thead>
                      <tr style={{backgroundColor: '#f5f5f5'}}>
                        {Object.keys(data.ev_data[0]).map(key => (
                          <th key={key} style={{border: '1px solid #ddd', padding: '12px', textAlign: 'left'}}>
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {data.ev_data.map((row, index) => (
                        <tr key={index}>
                          {Object.values(row).map((value, i) => (
                            <td key={i} style={{border: '1px solid #ddd', padding: '12px'}}>
                              {String(value)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        ) : data && data.length > 0 ? (
          <div style={{overflowX: 'auto'}}>
            <table style={{width: '100%', borderCollapse: 'collapse', marginTop: '10px'}}>
              <thead>
                <tr style={{backgroundColor: '#f5f5f5'}}>
                  {Object.keys(data[0]).map(key => (
                    <th key={key} style={{border: '1px solid #ddd', padding: '12px', textAlign: 'left'}}>
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, i) => (
                      <td key={i} style={{border: '1px solid #ddd', padding: '12px'}}>
                        {String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No data returned</p>
        )}
      </div>
    </div>
  );
};

export default QueryResults;
