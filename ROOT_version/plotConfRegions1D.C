#include <iostream>
#include <vector>
#include <algorithm>
#include <string.h>
#include <unistd.h>
#include "../atlasstyle/AtlasStyle.C"
#include "TMinuit.h"

// bool mySortFunction (const std::vector<double>& i, const std::vector<double>& j);
bool mySortFunction1D(const std::vector<double>& i, const std::vector<double>& j);
// TH2D *getCL(double cl, double xmin, double xmax, double ymin, double ymax, TH2D *hist);
TH1D *getCL1D(double cl, double xmin, double xmax, TH1D *hist);
void doWork1D(string measurement, std::vector< std::string > params);
std::vector< std::string > get_parameters(string path1);


void plotConfRegions1D(string inputfilepath1){
	// Don't display canvas
	gROOT->SetBatch(kTRUE);

   char cwd[1024];
   if (getcwd(cwd, sizeof(cwd)) != NULL)
       fprintf(stdout, "Current working dir: %s\n", cwd);
   else
       perror("getcwd() error");

   std::string filepath1 = "";
   filepath1.append(cwd).append("/").append(inputfilepath1);

	// Compute all plots
	std::vector< std::string > params = get_parameters(inputfilepath1);
  doWork1D(inputfilepath1, params);
}








void doWork1D(string measurement, std::vector< std::string > params){

  // Apply ATLAS histogram style
  SetAtlasStyle();
  
	// Define required constants
	// 68.3% and 95.5% Confidence levels
	double CL68 = 0.683;
	double CL95 = 0.955;

	int numCoeff = params.size();

	// Import path for EFTFitter results
	string tmpPath = measurement;//+"/result_plots.root";
	const char *resultPath = tmpPath.c_str();

	// Import TFile
	TFile *hist = new TFile(resultPath,"READ");

	// Loop through the available histograms
	for (int i = 0; i<numCoeff; i++){

		// Extract the histogram
    std::string hist_prefix="hist_0_";
    hist_prefix.append(params[i]);

		TH1D *h1 = (TH1D*)hist->Get(hist_prefix.c_str());

    double xmin = h1->GetXaxis()->GetXmin();
    double xmax = h1->GetXaxis()->GetXmax();
    int nbinsx = h1->GetNbinsX();

		// Create canvas to plot histogram
	  TCanvas *c2=new TCanvas("c2", "1D", nbinsx);

    TH1D *h1sig1;
    TH1D *h1sig2;
    TH1D *h1rest;

    h1sig1 = getCL1D(CL68, xmin, xmax, h1);
    h1sig2 = getCL1D(CL95, xmin, xmax, h1);
    h1rest = getCL1D(0.9999, xmin, xmax, h1);

    h1sig2->SetAxisRange(xmin, xmax, "X");
    
    std::string xaxisname;
    if (params[i].compare("cpq") == 0) {
      xaxisname="#font[52]{c_{\\phi Q}}";
    }
    else if (params[i].compare("cptbR") == 0) {
      xaxisname="#font[52]{c_{\\phi tb}}";
    }
    else if (params[i].compare("cptbI") == 0) {
      xaxisname="#font[52]{Im( c_{\\phi tb})}";
    }
    else if (params[i].compare("cbwR") == 0) {
      xaxisname="#font[52]{Re( c_{bW})}";
    }
    else if (params[i].compare("cbwI") == 0) {
      xaxisname="#font[52]{Im( c_{bW})}";
    }
    else if (params[i].compare("ctwR") == 0) {
      xaxisname="#font[52]{Re( c_{tW})}";
    }
    else if (params[i].compare("ctwI") == 0) {
      xaxisname="#font[52]{Im( c_{tW})}";
    }
    else if (params[i].compare("cqq") == 0) {
      xaxisname="#font[52]{{c_{Qq}^{3,1}}";
    }
    else if (params[i].compare("P") == 0) {
      xaxisname="#font[52]{Polarization}";
    }


    h1sig2->SetXTitle (xaxisname.c_str());
    std::string yaxisname = "#font[52]{p(";
    yaxisname.append(xaxisname).append("|data)}");
    h1sig2->SetYTitle (yaxisname.c_str());


		h1sig2->SetBit(TH1::kNoStats);

		// Draw the 68.3% CL region
		h1sig2->Draw("][");
		// h1sig2->Add(h1sig1,h1sig2,xmin,xmax);
		h1sig1->Draw("][ same");
		h1rest->Draw(" same");

		// Set all plot options
		h1sig1->SetMarkerStyle(20);
		h1sig2->SetMarkerStyle(20);
		h1rest->SetMarkerStyle(20);

		h1sig1->SetMarkerSize(0.6);
		h1sig2->SetMarkerSize(0.6);
		h1rest->SetMarkerSize(0.6);

		h1sig1->SetMarkerColor(3);
		h1sig2->SetMarkerColor(5);
		h1rest->SetMarkerColor(1);
    h1sig1->SetFillColor(3);
    h1sig2->SetFillColor(5);




	  auto legend = new TLegend(0.75,0.75,0.95,0.9); 
    legend->AddEntry((TObject*)0, "", "");
    legend->AddEntry(h1sig1,"#font[52]{68.3% CL}","f");//"#font[52]{p}_{x} [GeV]"
    legend->AddEntry((TObject*)0, "", "");
    legend->AddEntry(h1sig2,"#font[52]{95.5% CL}","f");
    legend->AddEntry((TObject*)0, "", "");
    legend->SetBorderSize(0);
    legend->SetFillStyle(0);

    gStyle->SetOptTitle(0);

    legend->Draw();

    h1sig2->GetYaxis()->SetTitleOffset(1.9);
    c2->SetLeftMargin(0.21);

    gPad->RedrawAxis();






    		// Set plot name
		string tmpPlotName = "#font[52]{Measurement: " + measurement + " - Couplings: " + params[i].c_str() + "}";
		const char *plotName = tmpPlotName.c_str();
		h1sig2->SetTitle (plotName);


		// Set pdf file name
		string path1 = "plots/1D/";
		path1.append(params[i].c_str()).append("_1D.pdf");

		// Export pdf
		c2->Print(path1.c_str());

		// Clean up
		delete h1;
		delete c2;
    delete h1sig1;
    delete h1sig2;
    // delete h1rest;
  }


  delete hist;
}


















// Get the available parameters
std::vector< std::string > get_parameters(string measurement){
  const char * c = measurement.c_str();

  TFile *f1 = TFile::Open(c);
  TIter next(f1->GetListOfKeys());
  TKey *key;
  TCanvas c1;

	// Available histograms from EFTFitter
  std::vector< std::string > availableComb;

  while ((key = (TKey*)next())) {
    TClass *cl = gROOT->GetClass(key->GetClassName());
    if (!cl->InheritsFrom("TH1")) continue;
    TH1 *h = (TH1*)key->ReadObj();


    std::string tmp_name = h->GetName();
    // std::cout << tmp_name << std::endl;
    if ( std::count(tmp_name.begin(), tmp_name.end(), '_') == 2 ){
      std::vector < std::string > tokens;
      // stringstream class check1 
      stringstream check1(tmp_name);
      std::string intermediate; 
      
      // Tokenizing w.r.t. space ' ' 
      while(getline(check1, intermediate, '_')) 
      { 
          tokens.push_back(intermediate); 
      } 
      std::string last = tokens.back();
      availableComb.push_back(last);
    }

  }
  // for (auto i = availableComb.begin(); i != availableComb.end(); ++i) {
  //   std::cout << (*i) << std::endl;
  // }
  return availableComb;
}



// Sorts the vector in descending order
bool mySortFunction1D(const std::vector<double>& i, const std::vector<double>& j)
{ 
	return (i[1]>j[1]);
}

// Compute the CL regions
TH1D *getCL1D(double cl, double xmin, double xmax, TH1D *hist){
	// Set names for histogram
	string histName = "Name: ";
	string histName2 = histName.append(hist->GetName()) + ", CL: " + to_string(cl);
	const char *name = histName2.c_str();

	// compute range of histogram
	double xrange = abs(xmin)+abs(xmax);

	//Calculate volume of 2D hist
	Double_t binx1 = hist->GetXaxis()->FindBin(xmin);
	Double_t binx2 = hist->GetXaxis()->FindBin(xmax);
	Double_t vol = hist->Integral(binx1, binx2);
  
    std::vector<std::vector<double>> vAll;
    //Fill vector with data from histogram
	for (int i = 1; i<=hist->GetNbinsX(); i++) {
				std::vector<Double_t> tmp = {(float)(i), hist->GetBinContent(i)};
				vAll.push_back(tmp);
	}

	//Sort vector in descending size
	sort(vAll.begin(), vAll.end(), mySortFunction1D);
	// for(int  i=0;i<vAll.size();i++){
	// 	std::cout << "vAll[" << i << "] = " << vAll[i][0] << " - " << vAll[i][1] << std::endl;
	// }

 	TH1D *hr = new TH1D(name, "cl", hist->GetNbinsX(), xmin, xmax);

 	//Fill the new histogram until CL% of the total volume has bee reached
	Double_t level1 = 0;
	Int_t counter = 0;
	while (level1<cl*vol) {
			level1 += vAll[counter][1];
      hr->SetBinContent((int)(vAll[counter][0]),vAll[counter][1]);
			counter++;
      if (counter==vAll.size()){
        break;
      }
	}
  // TCanvas *c2=new TCanvas("c3", "1D", hr->GetNbinsX());
	// 	hr->Draw("same");
  //   c2->Print("testhist.pdf");

	return hr;
}
