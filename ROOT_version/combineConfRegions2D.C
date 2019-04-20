#include <iostream>
#include <vector>
#include <algorithm>
#include <string.h>
#include <unistd.h>
#include "../atlasstyle/AtlasStyle.C"



bool mySortFunction (const std::vector<double>& i, const std::vector<double>& j);
TH2D *getCL(double cl, double xmin, double xmax, double ymin, double ymax, TH2D *hist);
std::vector< std::string > get_parameters(string measurement);
void doWork2D(string measurement1, string measurement2, std::vector< std::string > params1, std::vector< std::string > params2);
vector<string> split (const string &s, char delim);


void combineConfRegions2D(string inputfilepath1, string inputfilepath2){
	// Don't display canvas
	gROOT->SetBatch(kTRUE);

   char cwd[1024];
   if (getcwd(cwd, sizeof(cwd)) != NULL)
       fprintf(stdout, "Current working dir: %s\n", cwd);
   else
       perror("getcwd() error");

   std::string filepath1 = "";
   std::string filepath2 = "";
   filepath1.append(cwd).append("/").append(inputfilepath1);
   filepath2.append(cwd).append("/").append(inputfilepath2);

	// Compute all plots
	std::vector< std::string > params1 = get_parameters(inputfilepath1);
	std::vector< std::string > params2 = get_parameters(inputfilepath2);
  doWork2D(inputfilepath1, inputfilepath2, params1, params2);
}








void doWork2D(string measurement1, string measurement2, std::vector< std::string > params1, std::vector< std::string > params2){

  // Apply ATLAS histogram style
  SetAtlasStyle();
  
	// Define required constants
	// 68.3% and 95.5% Confidence levels
	double CL68 = 0.683;
	double CL95 = 0.955;

	int numCoeff = params1.size();

	// Import path for EFTFitter results
	string tmpPath1 = measurement1;//+"/result_plots.root";
	string tmpPath2 = measurement2;//+"/result_plots.root";
	const char *resultPath1 = tmpPath1.c_str();
	const char *resultPath2 = tmpPath2.c_str();

	// Import TFiles
	TFile *hist1 = new TFile(resultPath1,"READ");
	TFile *hist2 = new TFile(resultPath2,"READ");

	// Loop through the available histograms
	for (int i = 0; i<numCoeff; i++){

		// Extract the histogram
    std::string hist_prefix="hist_0_";
    hist_prefix.append(params1[i]);

		TH2D *h1 = (TH2D*)hist1->Get(hist_prefix.c_str());
		TH2D *h2 = (TH2D*)hist2->Get(hist_prefix.c_str());

    double xmin = h1->GetXaxis()->GetXmin();
    double xmax = h1->GetXaxis()->GetXmax();
    double ymin = h1->GetYaxis()->GetXmin();
    double ymax = h1->GetYaxis()->GetXmax();
    int binx = h1->GetNbinsX();

		// Create canvas to plot histogram
	  TCanvas *c1=new TCanvas("c1", "2D", binx);

    TH2D *h1sig1;
    TH2D *h1sig2;
    
		h1sig1 = getCL(CL95, xmin, xmax, ymin, ymax, h1);
		h1sig2 = getCL(CL95, xmin, xmax, ymin, ymax, h2);

    h1sig2->SetAxisRange(xmin, xmax, "X");
    h1sig2->SetAxisRange(ymin, ymax, "Y");
    // h1sig2->SetAxisRange(-3, 3, "X");
    // h1sig2->SetAxisRange(-3, 3, "Y");

		h1sig2->SetBit(TH1::kNoStats);

		// Draw the 68.3% CL region
		h1sig2->Draw("][");
		// h1sig2->Add(h1sig1,h1sig2,xmin,xmax);
		h1sig1->Draw("][ same");
		// h1rest->Draw("same");


		char delim='_';
    std::string xname =   split (params1[i], delim)[0];
    std::string yname =   split (params2[i], delim)[1];
    std::string xaxisname;
    if (xname.compare("cpq") == 0) {
      xaxisname="#font[52]{c_{\\phi Q}}";
    }
    else if (xname.compare("cptbR") == 0) {
      xaxisname="#font[52]{c_{\\phi tb}}";
    }
    else if (xname.compare("cptbI") == 0) {
      xaxisname="#font[52]{Im( c_{\\phi tb})}";
    }
    else if (xname.compare("cbwR") == 0) {
      xaxisname="#font[52]{Re( c_{bW})}";
    }
    else if (xname.compare("cbwI") == 0) {
      xaxisname="#font[52]{Im( c_{bW})}";
    }
    else if (xname.compare("ctwR") == 0) {
      xaxisname="#font[52]{Re( c_{tW})}";
    }
    else if (xname.compare("ctwI") == 0) {
      xaxisname="#font[52]{Im( c_{tW})}";
    }
    else if (xname.compare("cqq") == 0) {
      xaxisname="#font[52]{c_{Qq}^{3,1}}";
    }
    else if (xname.compare("P") == 0) {
      xaxisname="#font[52]{Polarization}";
    }

    std::string yaxisname;
    if (yname.compare("cpq") == 0) {
      yaxisname="#font[52]{c_{\\phi Q}}";
    }
    else if (yname.compare("cptbR") == 0) {
      yaxisname="#font[52]{c_{\\phi tb}}";
    }
    else if (yname.compare("cptbI") == 0) {
      yaxisname="#font[52]{Im( c_{\\phi tb})}";
    }
    else if (yname.compare("cbwR") == 0) {
      yaxisname="#font[52]{Re( c_{bW})}";
    }
    else if (yname.compare("cbwI") == 0) {
      yaxisname="#font[52]{Imleft( c_{bW})}";
    }
    else if (yname.compare("ctwR") == 0) {
      yaxisname="#font[52]{Re( c_{tW})}";
    }
    else if (yname.compare("ctwI") == 0) {
      yaxisname="#font[52]{Im( c_{tW})}";
    }
    else if (yname.compare("cqq") == 0) {
      yaxisname="#font[52]{c_{Qq}^{3,1}}";
    }
    else if (yname.compare("P") == 0) {
      yaxisname="#font[52]{Polarization}";
    }

		h1sig2->SetXTitle (xaxisname.c_str());
		h1sig2->SetYTitle (yaxisname.c_str());




		// Set all plot options
		h1sig1->SetMarkerStyle(20);
		h1sig2->SetMarkerStyle(20);
		// h1rest->SetMarkerStyle(20);

		h1sig1->SetMarkerSize(0.6);
		h1sig2->SetMarkerSize(0.6);
		// h1rest->SetMarkerSize(0.6);

		h1sig1->SetMarkerColor(kAzure+10);
		h1sig2->SetMarkerColor(kOrange+7);
		// h1rest->SetMarkerColor(1);
    h1sig1->SetFillColor(kAzure+10);
    h1sig2->SetFillColor(kOrange+7);




	  auto legend = new TLegend(0.75,0.75,0.95,0.95); 
    legend->AddEntry((TObject*)0, "", "");
    legend->AddEntry(h1sig1,"#font[52]{Fiducial Cross Section}","f");
    legend->AddEntry((TObject*)0, "", "");
    legend->AddEntry(h1sig2,"#font[52]{Total Cross Section}","f");
    legend->AddEntry((TObject*)0, "", "");
    legend->SetBorderSize(0);
    legend->SetFillStyle(0);

    gStyle->SetOptTitle(0);

    legend->Draw();

    h1sig2->GetYaxis()->SetTitleOffset(1.8);
    c2->SetLeftMargin(0.2);






    		// Set plot name
		string tmpPlotName = "#font[52]{Measurement: " + measurement1 + " - Couplings: " + params1[i].c_str() + "}";
		const char *plotName = tmpPlotName.c_str();
		h1sig2->SetTitle (plotName);


		// Set pdf file name
		string path1 = "plots/2D_comb/";
		path1.append(params1[i].c_str()).append("_2D.pdf");

		// Export pdf
		c1->Print(path1.c_str());




		delete h1;
		delete h2;
		delete c1;
    delete h1sig1;
    delete h1sig2;

  }
  delete hist1;
  delete hist2;
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
    if ( std::count(tmp_name.begin(), tmp_name.end(), '_') == 3 ){
      std::vector < std::string > tokens;
      // stringstream class check1 
      stringstream check1(tmp_name);
      std::string intermediate; 
      
      // Tokenizing w.r.t. space ' ' 
      while(getline(check1, intermediate, '0')) 
      { 
          tokens.push_back(intermediate); 
      } 
      std::string last = tokens.back();
      availableComb.push_back(last.erase(0,1));
    }

  }
  // for (auto i = availableComb.begin(); i != availableComb.end(); ++i) {
  //   std::cout << (*i) << std::endl;
  // }
  return availableComb;
}







// Sorts the vector in descending order
bool mySortFunction (const std::vector<double>& i, const std::vector<double>& j)
{ 
	return (i[2]>j[2]);
}

// Compute the CL regions
TH2D *getCL(double cl, double xmin, double xmax, double ymin, double ymax, TH2D *hist){

	// Set names for histogram
  auto rnd = std::to_string(rand());
	string histName = "Name: ";
	string histName2 = histName.append(hist->GetName()) + ", CL: " + to_string(cl) + "_" + rnd;
	const char *name = histName2.c_str();

	// compute range of histogram
	double xrange = abs(xmin)+abs(xmax);
	double yrange = abs(ymin)+abs(ymax);

	//Calculate volume of 2D hist
	Double_t binx1 = hist->GetXaxis()->FindBin(xmin);
	Double_t binx2 = hist->GetXaxis()->FindBin(xmax);
	Double_t biny1 = hist->GetYaxis()->FindBin(xmin);
	Double_t biny2 = hist->GetYaxis()->FindBin(ymax);
	Double_t vol = hist->Integral(binx1, binx2, biny1, biny2);

    std::vector<std::vector<double>> vAll;

    //Fill vector with data from histogram
	for (int i = 1; i<hist->GetNbinsX(); i++) {
		for (int j = 1; j<hist->GetNbinsY(); j++) {
			if(hist->GetBinContent(i,j)!=0){
				std::vector<Double_t> tmp = {(float)(i), (float)(j), hist->GetBinContent(i,j)};
				vAll.push_back(tmp);
			}
		}
	}

	//Sort vector in descending size
	sort(vAll.begin(), vAll.end(), mySortFunction);  

 	TH2D *hr = new TH2D(name, "cl", hist->GetNbinsX(), xmin, xmax, hist->GetNbinsY(), ymin, ymax);

 	//Fill the new histogram until CL% of the total volume has bee reached
	Double_t level1 = 0;
	Int_t counter = 0;
	while (level1<cl*vol) {
			level1 += vAll[counter][2];
			hr->SetBinContent((int)(vAll[counter][0]),(int)(vAll[counter][1]),1.);
			counter++;
	}
  
	return hr;
}





vector<string> split (const string &s, char delim) {
    vector<string> result;
    stringstream ss (s);
    string item;

    while (getline (ss, item, delim)) {
        result.push_back (item);
    }

    return result;
}
