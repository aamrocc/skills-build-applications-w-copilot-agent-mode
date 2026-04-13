import React, { useState, useEffect } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;
        console.log('Fetching Activities from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Activities API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const activitiesList = data.results || data || [];
        console.log('Processed Activities:', activitiesList);
        
        setActivities(activitiesList);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Loading activities...</p>
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
            <i className="bi bi-activity"></i> Activities
          </h1>
          
          {activities.length === 0 ? (
            <div className="card">
              <div className="card-body text-center py-5">
                <p className="text-muted">No activities found</p>
              </div>
            </div>
          ) : (
            <div className="table-container">
              <table className="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Activity Type</th>
                    <th>Duration</th>
                    <th>Date</th>
                    <th>User</th>
                    <th>Team</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {activities.map((activity) => (
                    <tr key={activity.id}>
                      <td>
                        <span className="badge bg-primary">{activity.id}</span>
                      </td>
                      <td>
                        <strong>{activity.activity_type}</strong>
                      </td>
                      <td>
                        <span className="badge bg-info">{activity.duration} min</span>
                      </td>
                      <td>{activity.date}</td>
                      <td>
                        <span className="badge bg-secondary">{activity.user_name}</span>
                      </td>
                      <td>
                        <span className="badge bg-success">{activity.team_name}</span>
                      </td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => setSelectedActivity(activity)}
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

          {selectedActivity && (
            <div className="card mt-4 shadow-sm">
              <div className="card-header d-flex justify-content-between align-items-center">
                <div>
                  <h5 className="mb-0">Activity Details</h5>
                  <small className="text-muted">ID: {selectedActivity.id}</small>
                </div>
                <button
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => setSelectedActivity(null)}
                >
                  Close
                </button>
              </div>
              <div className="card-body">
                <p>
                  <strong>Activity:</strong> {selectedActivity.activity_type}
                </p>
                <p>
                  <strong>Duration:</strong> {selectedActivity.duration} min
                </p>
                <p>
                  <strong>Date:</strong> {selectedActivity.date}
                </p>
                <p>
                  <strong>User:</strong> {selectedActivity.user_name || '-'}
                </p>
                <p>
                  <strong>Team:</strong> {selectedActivity.team_name || '-'}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Activities;
