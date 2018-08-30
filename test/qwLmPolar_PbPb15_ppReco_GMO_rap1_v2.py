import FWCore.ParameterSet.Config as cms

process = cms.Process("LmPolar")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v13', '')

process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco_GMOV0.root"),
        secondaryFileNames = cms.untracked.vstring(
            'file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root'
            ),
        )

process.TFileService = cms.Service("TFileService",
        fileName = cms.string('lmpolar.root')
        )

process.QWVertex = cms.EDProducer('QWVertexProducer',
        vertexSrc = cms.untracked.InputTag('GMOVertex')
        )

process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
        vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
        )

process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
        src = cms.untracked.InputTag('QWPrimaryVz'),
        dmin = cms.untracked.double(-15.),
        dmax = cms.untracked.double(15.),
        )

process.QWPrimaryVertexSelection = cms.Sequence( process.QWVertex * process.QWPrimaryVz * process.QWVzFilter15 )

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')

process.NoffFilter60 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(60, 180)
            ),
        BinLabel = cms.InputTag("centralityBins")
        )

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
	+ process.QWPrimaryVertexSelection
        #        + process.primaryVertexFilter
        #        + process.clusterCompatibilityFilter
        )


process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('GMOVertex')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.9998)
                , ptMin = cms.untracked.double(0.2)
		, ptMax = cms.untracked.double(1.0)
		, Rapmin = cms.untracked.double(-1.0)
		, Rapmax = cms.untracked.double(1.0)
                ),
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.9999)
                , ptMin = cms.untracked.double(1.0)
                , ptMax = cms.untracked.double(8.5)
		, Rapmin = cms.untracked.double(-1.0)
		, Rapmax = cms.untracked.double(1.0)
                )
            )
        )

process.lmpolar = cms.EDAnalyzer('QWLmPolar',
		centrality = cms.untracked.InputTag('centralityBins'),
		pdgId = cms.untracked.InputTag('QWV0EventLambda', 'pdgId'),
		pPhiCM = cms.untracked.InputTag('QWV0EventLambda', 'pPhiCM'),
		nPhiCM = cms.untracked.InputTag('QWV0EventLambda', 'nPhiCM'),
		mixNoffBins = cms.untracked.vint32(0, 60, 80, 100, 120, 160, 200),
		Nmix = cms.untracked.uint32(20)
	)

process.load('PbPb_HIMB5_ppReco_eff')

process.ana = cms.Path(
        process.eventSelection
        * process.centralityBins
        * process.NoffFilter60
        * process.QWV0EventLambda
        * process.lmpolar
        )

process.RECO = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('drop *',
            'keep *_*_*_LmPolar'),
        SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring('ana')
            ),
        fileName = cms.untracked.string('recoV0.root')
        )


process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
        process.ana,
#        process.out
        )


