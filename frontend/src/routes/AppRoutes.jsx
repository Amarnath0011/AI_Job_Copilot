import { Route,Routes } from "react-router-dom";
import LandingPage from "../pages/LandingPage";
import Dashboard from "../pages/Dashboard";
import MainLayout from "../layouts/MainLayOut";
import ResumePage from "../pages/ResumePage";
import InterviewPage from "../pages/InterviewPage";
import ReportPage from "../pages/ReportPage";


const AppRoutes = () => {

  
  return (
    <Routes>
            <Route element = {<MainLayout/>}>
             <Route path='/' element= {<LandingPage/>} ></Route>
             <Route path='/dashBoard' element = {<Dashboard/>}></Route>
             <Route path='/resume' element = {<ResumePage/>}></Route>
             <Route path='/interview' element = {<InterviewPage/>}></Route>
             <Route path='/report' element = {<ReportPage/>}></Route>

             
             </Route>
    </Routes>

  );
}

export default AppRoutes

