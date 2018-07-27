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

	private:
		virtual void beginJob() override;
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
		virtual void endJob() override;

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
	centralityTag_( iConfig.getUntrackedParameter<edm::InputTag>("centrality") )
{
        consumes<int>(centralityTag_);

	edm::Service<TFileService> fs;
	trV = fs->make<TTree>("trV", "trV");
	trV->Branch("Noff", &gNoff, "Noff/I");
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

	vLmLm.clear();
	vLmLmBar.clear();
	vLmBarLmBar.clear();

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
