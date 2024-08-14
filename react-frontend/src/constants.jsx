export const columns = [
    {
        title: 'Job Title',
        dataIndex: 'title',
        key: 'title',
        render: (_, record) => <a href={record.link} rel="noopener noreferrer">{record.title}</a>,
    },
    {
        title: 'Company',
        dataIndex: 'company',
        key: 'company',
    },
    {
        title: 'Location',
        dataIndex: 'location',
        key: 'location',
    },
    {
        title: 'Date Posted',
        dataIndex: 'date',
        key: 'date',
    },
];