import { useState } from "react";
import { Link } from "react-router-dom";

const Banner = () => {
  return (
    <div className="container-fluid p-5 text-center">
      <h1>Detect every performance change.</h1>
      <h5>
        The performance measurement tool that harnesses the power of change
        point detection
      </h5>
    </div>
  );
};

const FeatureHighlight = () => {
  return (
    <div className="row">
      <div className="col-sm-4">
        <h3>Shift left</h3>
        <p>
          Performance regressions are often only discovered during later stages
          of development such as release candidate testing.
        </p>
        <p>
          Pull your performance testing earlier with Nyrkiö and flag regressions
          as soon as they're committed.
        </p>
      </div>
      <div className="col-sm-4">
        <h3>Automate analysis</h3>
        <p>
          Avoid the tedious work of checking performance dashboards by hand.
        </p>
      </div>
      <div className="col-sm-4">
        <h3>State of the art</h3>
        <p>
          Change point detection is state of the art technology for detecting
          changes in software performance. Used by leading technology companies
          such all around the world including MongoDB and Netflix.
        </p>
      </div>
    </div>
  );
};

const LearnMore = () => {
  return (
    <div className="container p-5">
      <div className="row">
        <h3>Want to learn more?</h3>
        <Link to="/product">Read about the product here</Link>
      </div>
    </div>
  );
};

export const FrontPage = () => {
  return (
    <>
      <div className="container mt-5 text-center">
        <Banner />
        <FeatureHighlight />
        <button className="btn btn-success">
          <a className="btn-link" href="/signup">
            Sign up
          </a>
        </button>
        <LearnMore />
      </div>
      <></>
    </>
  );
};
