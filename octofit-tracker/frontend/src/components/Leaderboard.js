import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Fetching Leaderboard from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardList = data.results || data || [];
        console.log('Processed Leaderboard:', leaderboardList);
        
        setLeaderboard(leaderboardList);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          <strong>Error:</strong> {error}
          <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-lg-12">
          <h1 className="mb-4">
            <i className="bi bi-trophy"></i> Leaderboard
          </h1>
          
          {leaderboard.length === 0 ? (
            <div className="card">
              <div className="card-body text-center py-5">
                <p className="text-muted">No leaderboard data found</p>
              </div>
            </div>
          ) : (
            <div className="table-container">
              <table className="table table-hover mb-0">
                <thead>
                  <tr>
                    <th style={{ width: '80px' }}>Rank</th>
                    <th>User</th>
                    <th>Points</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry.id}>
                      <td>
                        <span className="badge bg-warning text-dark">
                          #{index + 1}
                        </span>
                      </td>
                      <td>
                        <strong>{entry.user_name}</strong>
                        {entry.team_name && (
                          <div className="small text-muted">{entry.team_name}</div>
                        )}
                      </td>
                      <td>
                        <span className="badge bg-success">
                          {entry.total_duration} min
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => setSelectedEntry(entry)}
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {selectedEntry && (
            <div className="card mt-4 shadow-sm">
              <div className="card-header d-flex justify-content-between align-items-center">
                <div>
                  <h5 className="mb-0">Leaderboard Entry</h5>
                  <small className="text-muted">ID: {selectedEntry.id}</small>
                </div>
                <button
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => setSelectedEntry(null)}
                >
                  Close
                </button>
              </div>
              <div className="card-body">
                <p><strong>User:</strong> {selectedEntry.user_name}</p>
                <p><strong>Team:</strong> {selectedEntry.team_name || '-'}</p>
                <p><strong>Total Duration:</strong> {selectedEntry.total_duration} min</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
