import React from 'react';

const tabs = [
    { key: 'Master', label: 'All' },
    { key: 'Technology', label: 'Technology' },
    { key: 'Business', label: 'Business' },
    { key: 'Engineering', label: 'Engineering' },
    { key: 'Government', label: 'Government' }
];

const Tab = ({ tab, activeTab, onClick }) => (
    <li key={tab.key} className={`border-b-2 ${activeTab === tab.key ? "border-indigo-600 text-indigo-600" : "border-white text-gray-500"}`}>
        <button
            role="tab"
            className="py-2.5 px-4 rounded-lg duration-150 bg-white hover:text-indigo-600 hover:bg-gray-50 active:bg-gray-100 font-medium"
            onClick={() => onClick(tab.key)}
        >
            {tab.label}
        </button>
    </li>
);

const TabList = ({ activeTab, setActiveTab }) => {
    return (
        <ul className="w-full mx-2 flex items-center gap-x-3 overflow-x-auto">
            {tabs.map(tab => (
                <Tab
                    key={tab.key}
                    tab={tab}
                    activeTab={activeTab}
                    onClick={setActiveTab}
                />
            ))}
        </ul>
    );
};

export default TabList;