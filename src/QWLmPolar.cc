#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include "TH1.h"

#include <iostream>


class
QWLmPolar : public edm::EDAnalyzer {
	public:
		explicit QWLmPolar(const edm::ParameterSet&);
		~QWLmPolar();

	private:
		virtual void beginJob() override {};
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
		virtual void endJob() override {};


	/////////////
		edm::InputTag		centralityTag_;
		edm::InputTag		pdgId_;
		edm::InputTag		pPhiCM_;
		edm::InputTag		nPhiCM_;

		TTree*			trV;
		std::vector<double>	v1LmLm;
		std::vector<double>	v1LmBarLmBar;
		std::vector<double>	v1LmLmBar;

		std::vector<double>	v2LmLm;
		std::vector<double>	v2LmBarLmBar;
		std::vector<double>	v2LmLmBar;

		int			Noff;
		int			gV0;
};


QWLmPolar::QWLmPolar(const edm::ParameterSet& iConfig):
	centralityTag_( iConfig.getUntrackedParameter<edm::InputTag>("centrality") ),
	pdgId_( iConfig.getUntrackedParameter<edm::InputTag>("pdgId") ),
	pPhiCM_( iConfig.getUntrackedParameter<edm::InputTag>("pPhiCM") ),
	nPhiCM_( iConfig.getUntrackedParameter<edm::InputTag>("nPhiCM") )
{
	consumes<int>(centralityTag_);
	consumes<std::vector<double>>(pdgId_);
	consumes<std::vector<double>>(pPhiCM_);
	consumes<std::vector<double>>(nPhiCM_);

	edm::Service<TFileService> fs;
	trV = fs->make<TTree>("trV", "trV");
	trV->Branch("Noff", &Noff, "Noff/I");
	trV->Branch("NV0", &gV0, "gV0/I");

	trV->Branch("v1LmLm",		&v1LmLm);
	trV->Branch("v1LmBarLmBar",	&v1LmBarLmBar);
	trV->Branch("v1LmLmBar",	&v1LmLmBar);

	trV->Branch("v2LmLm",		&v2LmLm);
	trV->Branch("v2LmBarLmBar",	&v2LmBarLmBar);
	trV->Branch("v2LmLmBar",	&v2LmLmBar);
}

void
QWLmPolar::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;

	edm::Handle<std::vector<double>> hpdgId;
	iEvent.getByLabel(pdgId_, hpdgId);
	gV0 = hpdgId->size();
	if ( gV0 < 2 ) return;

	edm::Handle<int> ch;
	iEvent.getByLabel(centralityTag_,ch);
	Noff = *ch;

	v1LmLm.clear();
	v1LmLmBar.clear();
	v1LmBarLmBar.clear();
	v2LmLm.clear();
	v2LmLmBar.clear();
	v2LmBarLmBar.clear();

	edm::Handle<std::vector<double>> hpPhiCM;
	edm::Handle<std::vector<double>> hnPhiCM;

	iEvent.getByLabel(pPhiCM_, hpPhiCM);
	iEvent.getByLabel(nPhiCM_, hnPhiCM);


	for ( int i = 0; i < gV0; i++ ) {
		for ( int j = i+1; j < gV0; j++ ) {
			double ipPhi = (*hpPhiCM)[i];
			double inPhi = (*hnPhiCM)[i];
			double jpPhi = (*hpPhiCM)[j];
			double jnPhi = (*hnPhiCM)[j];

			if ( ( (*hpdgId)[i] == 3122 ) and ( (*hpdgId)[j] == 3122 ) ) {
				// Lm + Lm
				v1LmLm.emplace_back(cos(ipPhi - jpPhi));
				v2LmLm.emplace_back(cos(2*(ipPhi - jpPhi)));
			}
			if ( ( (*hpdgId)[i] == -3122 ) and ( (*hpdgId)[j] == -3122 ) ) {
				// LmBar + LmBar
				v1LmBarLmBar.emplace_back(cos(inPhi - jnPhi));
				v2LmBarLmBar.emplace_back(cos(2*(inPhi - jnPhi)));
			}
			if ( ( (*hpdgId)[i] == 3122 ) and ( (*hpdgId)[j] == -3122 ) ) {
				// Lm + LmBar
				v1LmLmBar.emplace_back(cos(ipPhi - jnPhi));
				v2LmLmBar.emplace_back(cos(2*(ipPhi - jnPhi)));
			}
			if ( ( (*hpdgId)[i] == -3122 ) and ( (*hpdgId)[j] == 3122 ) ) {
				// LmBar + Lm
				v1LmLmBar.emplace_back(cos(-inPhi+jpPhi));
				v2LmLmBar.emplace_back(cos(2*(-inPhi+jpPhi)));
			}
		}
	}

	trV->Fill();
}

QWLmPolar::~QWLmPolar()
{
}

DEFINE_FWK_MODULE(QWLmPolar);
