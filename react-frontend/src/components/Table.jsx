import React, { useEffect, useState } from 'react';
import { ConfigProvider, Table } from "antd";
import { columns } from '../constants.jsx';

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
        <ConfigProvider
            theme={{
                components: {
                    Table: {
                        headerBg: "white",
                    },
                },
            }}
        >
            <Table dataSource={masterTable} columns = {columns} />
        </ConfigProvider>
        
    );
};

export default JobListings;
