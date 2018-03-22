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
process.MessageLogger.cerr.FwkReport.reportEvery = 100

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
        BinLabel = cms.InputTag("Noff")
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
                ),
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.9999)
                , ptMin = cms.untracked.double(1.0)
                , ptMax = cms.untracked.double(8.5)
                )
            )
        )


# HF a 3.0 - 3.5
# HF b 3.5 - 4.0
# HF c 4.0 - 4.5
# HF d 4.5 - 5.0
# HF e 3.0 - 4.0 = a+b
# HF f 4.0 - 5.0 = c+d
# HF g 3.0 - 5.0 = a+b+c+d

process.CaloQ1a = cms.EDProducer('QWCaloQProducer',
        caloSrc = cms.untracked.InputTag('towerMaker'),
        etaMin = cms.untracked.double(3.0),
        etaMax = cms.untracked.double(3.5),
        N = cms.untracked.int32(1)
        )

process.CaloQ1b = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(3.5),
        etaMax = cms.untracked.double(4.0),
        )

process.CaloQ1c = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(4.0),
        etaMax = cms.untracked.double(4.5),
        )

process.CaloQ1d = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(4.5),
        etaMax = cms.untracked.double(5.0),
        )

process.CaloQ1e = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(3.0),
        etaMax = cms.untracked.double(4.0),
        )

process.CaloQ1f = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(4.0),
        etaMax = cms.untracked.double(5.0),
        )

process.CaloQ1g = process.CaloQ1a.clone(
        etaMin = cms.untracked.double(3.0),
        etaMax = cms.untracked.double(5.0),
        )

process.CaloQ2a = process.CaloQ1a.clone( N = cms.untracked.int32(2) )
process.CaloQ2b = process.CaloQ1b.clone( N = cms.untracked.int32(2) )
process.CaloQ2c = process.CaloQ1c.clone( N = cms.untracked.int32(2) )
process.CaloQ2d = process.CaloQ1d.clone( N = cms.untracked.int32(2) )
process.CaloQ2e = process.CaloQ1e.clone( N = cms.untracked.int32(2) )
process.CaloQ2f = process.CaloQ1f.clone( N = cms.untracked.int32(2) )
process.CaloQ2g = process.CaloQ1g.clone( N = cms.untracked.int32(2) )

process.caloQ = cms.Sequence( process.CaloQ1a + process.CaloQ1b + process.CaloQ1c + process.CaloQ1d + process.CaloQ1e + process.CaloQ1f + process.CaloQ1g
        + process.CaloQ2a + process.CaloQ2b + process.CaloQ2c + process.CaloQ2d + process.CaloQ2e + process.CaloQ2f + process.CaloQ2g
        )


process.load('PbPb_HIMB5_ppReco_eff')


process.LmTree = cms.EDAnalyzer('QWTreeMaker',
        src = cms.untracked.InputTag('QWV0EventLambda'),
        vTag = cms.untracked.vstring('phi', 'eta', 'rapidity', 'pt', 'mass', 'weight', 'pdgId', 'pPhiCM', 'nPhiCM')
        )

process.CaloTree = cms.EDAnalyzer('QWDTagTreeMaker',
        vTag = cms.untracked.VInputTag(
            cms.untracked.InputTag('CaloQ1a', 'arg'),
            cms.untracked.InputTag('CaloQ1a', 'argp'),
            cms.untracked.InputTag('CaloQ1a', 'argm'),
            cms.untracked.InputTag('CaloQ1a', 'abs'),
            cms.untracked.InputTag('CaloQ1a', 'absp'),
            cms.untracked.InputTag('CaloQ1a', 'absm'),

            cms.untracked.InputTag('CaloQ1b', 'arg'),
            cms.untracked.InputTag('CaloQ1b', 'argp'),
            cms.untracked.InputTag('CaloQ1b', 'argm'),
            cms.untracked.InputTag('CaloQ1b', 'abs'),
            cms.untracked.InputTag('CaloQ1b', 'absp'),
            cms.untracked.InputTag('CaloQ1b', 'absm'),

            cms.untracked.InputTag('CaloQ1c', 'arg'),
            cms.untracked.InputTag('CaloQ1c', 'argp'),
            cms.untracked.InputTag('CaloQ1c', 'argm'),
            cms.untracked.InputTag('CaloQ1c', 'abs'),
            cms.untracked.InputTag('CaloQ1c', 'absp'),
            cms.untracked.InputTag('CaloQ1c', 'absm'),

            cms.untracked.InputTag('CaloQ1d', 'arg'),
            cms.untracked.InputTag('CaloQ1d', 'argp'),
            cms.untracked.InputTag('CaloQ1d', 'argm'),
            cms.untracked.InputTag('CaloQ1d', 'abs'),
            cms.untracked.InputTag('CaloQ1d', 'absp'),
            cms.untracked.InputTag('CaloQ1d', 'absm'),

            cms.untracked.InputTag('CaloQ1e', 'arg'),
            cms.untracked.InputTag('CaloQ1e', 'argp'),
            cms.untracked.InputTag('CaloQ1e', 'argm'),
            cms.untracked.InputTag('CaloQ1e', 'abs'),
            cms.untracked.InputTag('CaloQ1e', 'absp'),
            cms.untracked.InputTag('CaloQ1e', 'absm'),

            cms.untracked.InputTag('CaloQ1f', 'arg'),
            cms.untracked.InputTag('CaloQ1f', 'argp'),
            cms.untracked.InputTag('CaloQ1f', 'argm'),
            cms.untracked.InputTag('CaloQ1f', 'abs'),
            cms.untracked.InputTag('CaloQ1f', 'absp'),
            cms.untracked.InputTag('CaloQ1f', 'absm'),

            cms.untracked.InputTag('CaloQ1g', 'arg'),
            cms.untracked.InputTag('CaloQ1g', 'argp'),
            cms.untracked.InputTag('CaloQ1g', 'argm'),
            cms.untracked.InputTag('CaloQ1g', 'abs'),
            cms.untracked.InputTag('CaloQ1g', 'absp'),
            cms.untracked.InputTag('CaloQ1g', 'absm'),

            cms.untracked.InputTag('CaloQ2a', 'arg'),
            cms.untracked.InputTag('CaloQ2a', 'argp'),
            cms.untracked.InputTag('CaloQ2a', 'argm'),
            cms.untracked.InputTag('CaloQ2a', 'abs'),
            cms.untracked.InputTag('CaloQ2a', 'absp'),
            cms.untracked.InputTag('CaloQ2a', 'absm'),

            cms.untracked.InputTag('CaloQ2b', 'arg'),
            cms.untracked.InputTag('CaloQ2b', 'argp'),
            cms.untracked.InputTag('CaloQ2b', 'argm'),
            cms.untracked.InputTag('CaloQ2b', 'abs'),
            cms.untracked.InputTag('CaloQ2b', 'absp'),
            cms.untracked.InputTag('CaloQ2b', 'absm'),

            cms.untracked.InputTag('CaloQ2c', 'arg'),
            cms.untracked.InputTag('CaloQ2c', 'argp'),
            cms.untracked.InputTag('CaloQ2c', 'argm'),
            cms.untracked.InputTag('CaloQ2c', 'abs'),
            cms.untracked.InputTag('CaloQ2c', 'absp'),
            cms.untracked.InputTag('CaloQ2c', 'absm'),

            cms.untracked.InputTag('CaloQ2d', 'arg'),
            cms.untracked.InputTag('CaloQ2d', 'argp'),
            cms.untracked.InputTag('CaloQ2d', 'argm'),
            cms.untracked.InputTag('CaloQ2d', 'abs'),
            cms.untracked.InputTag('CaloQ2d', 'absp'),
            cms.untracked.InputTag('CaloQ2d', 'absm'),

            cms.untracked.InputTag('CaloQ2e', 'arg'),
            cms.untracked.InputTag('CaloQ2e', 'argp'),
            cms.untracked.InputTag('CaloQ2e', 'argm'),
            cms.untracked.InputTag('CaloQ2e', 'abs'),
            cms.untracked.InputTag('CaloQ2e', 'absp'),
            cms.untracked.InputTag('CaloQ2e', 'absm'),

            cms.untracked.InputTag('CaloQ2f', 'arg'),
            cms.untracked.InputTag('CaloQ2f', 'argp'),
            cms.untracked.InputTag('CaloQ2f', 'argm'),
            cms.untracked.InputTag('CaloQ2f', 'abs'),
            cms.untracked.InputTag('CaloQ2f', 'absp'),
            cms.untracked.InputTag('CaloQ2f', 'absm'),

            cms.untracked.InputTag('CaloQ2g', 'arg'),
            cms.untracked.InputTag('CaloQ2g', 'argp'),
            cms.untracked.InputTag('CaloQ2g', 'argm'),
            cms.untracked.InputTag('CaloQ2g', 'abs'),
            cms.untracked.InputTag('CaloQ2g', 'absp'),
            cms.untracked.InputTag('CaloQ2g', 'absm'),
            )
        )

process.ana = cms.Path(
        process.eventSelection
        * process.centralityBins
        * process.NoffFilter60
        * process.QWV0EventLambda
        * process.caloQ
	* process.LmTree
        * process.CaloTree
        )

process.RECO = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('drop *',
            'keep *_*_*_CumuDiff'),
        SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring('ana250')
            ),
        fileName = cms.untracked.string('recoV0.root')
        )


process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
        process.ana,
#        process.out
        )
