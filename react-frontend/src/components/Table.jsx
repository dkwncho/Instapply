import React, { useEffect, useState } from 'react';

function JobListings() {
    const [masterTable, setMasterTable] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('https://instapply-api.vercel.app/api/master/cache')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setMasterTable(data);
                setLoading(false);
                console.log(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setError(error);
                setLoading(false);
            });
    }, []);
    
    if (loading) {
        return <p>Loading...</p>;
    }
    
    if (error) {
        return <p>Error fetching data: {error.message}</p>;
    }

    return (
        <div>
            <h1>Job Listings</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Company</th>
                        <th>Location</th>
                        <th>Date</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    {masterTable.map(job => (
                        <tr key={job.id}>
                            <td>{job.title}</td>
                            <td>{job.company}</td>
                            <td>{job.location}</td>
                            <td>{new Date(job.date).toLocaleDateString()}</td>
                            <td><a href={job.link} target="_blank" rel="noopener noreferrer">Apply</a></td>
                            </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default JobListings;
