import React, { useEffect, useState } from 'react';
import TabList from './TabList';

const filterByIndustry = (data, industry) => {
    if (!Array.isArray(data)) {
        return [];
    }
    return data.filter(item => item.industry.includes(industry));
};

function Table() {
    const [masterTable, setMasterTable] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState("Master");
    const [todayInternshipCount, setTodayInternshipCount] = useState(0);
    const today = new Date();
    var yesterday = new Date(today.setDate(today.getDate() - 1));
    yesterday = `${String(yesterday.getMonth() + 1).padStart(2, '0')}/${String(yesterday.getDate()).padStart(2, '0')}/${yesterday.getFullYear()}`;

    useEffect(() => {
        fetch('https://instapply-api.vercel.app/api/master/cache')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setMasterTable(data.reverse());
                setTodayInternshipCount(data.filter(item => item.date === yesterday).length);
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

    const activeTabTable = activeTab === "Master" ? masterTable : filterByIndustry(masterTable, activeTab);

    return (
        <div className="max-w-screen-xl mx-auto px-4 md:px-8">
            <div className="mx-2 max-w-lg text-left">
                <h3 className="title text-xl font-bold sm:text-2xl">
                    {todayInternshipCount} New Internships Added Today!
                </h3>
            </div>
            <div className="text-sm mt-6 overflow-x-auto">
                <TabList activeTab={activeTab} setActiveTab={setActiveTab} />
                <div className="shadow-sm border rounded-lg">
                    <table className="w-full table-auto rounded-lg text-left">
                        <thead className="bg-gray-50 text-gray-600 font-medium border-b">
                            <tr>
                                <th className="w-4/12 py-4 pl-6">Job Title</th>
                                <th className="w-3/12 py-4 pl-6">Company</th>
                                <th className="w-3.5/12 py-4 pl-6">Location</th>
                                <th className="w-1.5/12 py-4 pl-6">Date</th>
                            </tr>
                        </thead>
                        <tbody className="text-gray-600 divide-y">
                            {activeTabTable.map((item, idx) => (
                                    <tr key={idx}>
                                        <td className="pl-6 py-4 whitespace-wrap">
                                            <a href={item.link}>
                                                {item.title}
                                            </a>
                                        </td>
                                        <td className="pl-6 py-4 whitespace-wrap">{item.company}</td>
                                        <td className="pl-6 py-4 whitespace-wrap">{item.location}</td>
                                        <td className="pl-6 py-4 whitespace-wrap">{item.date}</td>
                                    </tr>
                                ))
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
};

export default Table;
