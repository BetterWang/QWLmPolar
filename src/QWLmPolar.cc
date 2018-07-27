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


class
QWLmPolar : public edm::EDAnalyzer {
	public:
		explicit QWLmPolar(const edm::ParameterSet&);
		~QWLmPolar();
		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions) {};

	private:
		virtual void beginJob();
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob();

		virtual void beginRun(edm::Run const&, edm::EventSetup const&) {};
		virtual void endRun(edm::Run const&, edm::EventSetup const&) {};
		virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) {};
		virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) {};

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
				v1LmLm.emplace_back(ipPhi - jpPhi);
				v2LmLm.emplace_back(2*(ipPhi - jpPhi));
			} else
			if ( ( (*hpdgId)[i] == -3122 ) and ( (*hpdgId)[j] == -3122 ) ) {
				// LmBar + LmBar
				v1LmLm.emplace_back(inPhi - jnPhi);
				v2LmLm.emplace_back(2*(inPhi - jnPhi));
			} else
			if ( ( (*hpdgId)[i] == 3122 ) and ( (*hpdgId)[j] == -3122 ) ) {
				// Lm + LmBar
				v1LmLm.emplace_back(ipPhi - jnPhi);
				v2LmLm.emplace_back(2*(ipPhi - jnPhi));
			} else
			if ( ( (*hpdgId)[i] == -3122 ) and ( (*hpdgId)[j] == 3122 ) ) {
				// LmBar + Lm
				v1LmLm.emplace_back(inPhi - jpPhi);
				v2LmLm.emplace_back(2*(inPhi - jpPhi));
			}
		}
	}

	trV->Fill();
}

DEFINE_FWK_MODULE(QWLmPolar);
