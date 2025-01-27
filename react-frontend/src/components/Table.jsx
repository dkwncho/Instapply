import React, { useEffect, useState } from "react";
import TabList from "./TabList";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookmark as solidBookmark } from "@fortawesome/free-solid-svg-icons";
import { faBookmark as regularBookmark } from "@fortawesome/free-regular-svg-icons";
import { faArrowLeft, faArrowRight } from "@fortawesome/free-solid-svg-icons"; // Added arrow icons

const filterByIndustry = (data, industry) => {
  if (!Array.isArray(data)) {
    return [];
  }
  return data.filter((item) => item.industry.includes(industry));
};

function Table() {
  const [masterTable, setMasterTable] = useState([]);
  const [activeTab, setActiveTab] = useState(() => {
    return localStorage.getItem("activeTab") || "Master";
  });
  const [savedJobs, setSavedJobs] = useState(() => {
    return JSON.parse(localStorage.getItem("savedJobs")) || [];
  });
  const [todayInternshipCount, setTodayInternshipCount] = useState(0);
  const today = new Date();
  var yesterday = new Date(today.setDate(today.getDate() - 1));
  yesterday = `${String(yesterday.getMonth() + 1).padStart(2, "0")}/${String(yesterday.getDate()).padStart(
    2,
    "0"
  )}/${yesterday.getFullYear()}`;

  const [pageStates, setPageStates] = useState({
    Master: 1,
    Technology: 1,
    Business: 1,
    Engineering: 1,
    Government: 1,
    Saved: 1,
  });

  const itemsPerPage = 50;

  const activeTabTable =
    activeTab === "Saved" ? savedJobs : activeTab === "Master" ? masterTable : filterByIndustry(masterTable, activeTab);

  const currentPage = pageStates[activeTab];
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return activeTabTable.slice(startIndex, endIndex);
  }, [activeTabTable, currentPage]);

  const totalPages = Math.max(1, Math.ceil(activeTabTable.length / itemsPerPage));

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    localStorage.setItem("activeTab", activeTab);
  }, [activeTab]);

  useEffect(() => {
    fetch("https://instapply-api.vercel.app/api/master/cache")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setMasterTable(data.reverse());
        setTodayInternshipCount(data.filter((item) => item.date === yesterday).length);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setError(error);
        setLoading(false);
      });
  }, []);

  const saveJob = (job) => {
    let updatedSavedJobs = [...savedJobs];
    const jobIndex = updatedSavedJobs.findIndex((savedJob) => savedJob.link === job.link);
    if (jobIndex > -1) {
      updatedSavedJobs.splice(jobIndex, 1);
    } else {
      updatedSavedJobs.push(job);
    }
    setSavedJobs(updatedSavedJobs);
    localStorage.setItem("savedJobs", JSON.stringify(updatedSavedJobs));
  };

  const isJobSaved = (job) => {
    return savedJobs.some((savedJob) => savedJob.link === job.link);
  };

  const handlePageChange = (newPage) => {
    setPageStates((prev) => ({
      ...prev,
      [activeTab]: newPage,
    }));
  };

  if (loading) {
    return (
      <div class="flex justify-center items-center w-full h-full">
        <div class="flex justify-center items-center space-x-1 text-sm text-gray-700">
          <svg fill="none" class="w-10 h-10 animate-spin" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <path
              clip-rule="evenodd"
              d="M15.165 8.53a.5.5 0 01-.404.58A7 7 0 1023 16a.5.5 0 011 0 8 8 0 11-9.416-7.874.5.5 0 01.58.404z"
              fill="currentColor"
              fill-rule="evenodd"
            />
          </svg>
          <div>Loading ...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return <p>Error fetching data: {error.message}</p>;
  }

  return (
    <div className="max-w-screen-xl mx-auto px-4 md:px-8">
      <div className="flex">
        <div className="mx-2 max-w-full text-left">
          <h3 className="title text-xl font-bold sm:text-2xl">{todayInternshipCount} New Internships Added Today!</h3>
        </div>
      </div>

      <div className="text-sm mt-6">
        <TabList activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="shadow-sm border rounded-lg">
          <table className="w-full table-auto rounded-lg text-left">
            <thead className="bg-gray-50 text-gray-600 font-medium border-b">
              <tr>
                <th className="w-4/12 py-4 pl-6">Job Title</th>
                <th className="w-3/12 py-4 pl-6">Company</th>
                <th className="w-3.5/12 py-4 pl-6">Location</th>
                <th className="w-1.5/12 py-4 px-6">Date</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 divide-y">
              {paginatedData.map((item, idx) => (
                <tr key={idx}>
                  <td className="pl-4 py-4 whitespace-wrap flex items-center">
                    <button onClick={() => saveJob(item)} className="mr-2 p-2 text-lg">
                      <FontAwesomeIcon icon={isJobSaved(item) ? solidBookmark : regularBookmark} />
                    </button>
                    <a href={item.link}>{item.title}</a>
                  </td>
                  <td className="pl-6 py-4 whitespace-wrap">{item.company}</td>
                  <td className="pl-6 py-4 whitespace-wrap">{item.location}</td>
                  <td className="px-6 py-4 whitespace-wrap">{item.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="flex justify-center items-center mt-4">
        <button
          onClick={() => handlePageChange(Math.max(currentPage - 1, 1))}
          disabled={currentPage === 1}
          className="py-2 px-4 bg-transparent rounded disabled:opacity-50"
        >
          <FontAwesomeIcon icon={faArrowLeft} />
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => handlePageChange(Math.min(currentPage + 1, totalPages))}
          disabled={currentPage === totalPages}
          className="py-2 px-4 bg-transparent rounded disabled:opacity-50"
        >
          <FontAwesomeIcon icon={faArrowRight} />
        </button>
      </div>
    </div>
  );
}

export default Table;
