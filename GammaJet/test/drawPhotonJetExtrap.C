#include <stdlib.h>
#include "DrawExtrap.h"
#include "fitTools.h"


bool useMCassoc_ = true;



int main(int argc, char* argv[]) {

  if( argc != 6 && argc!=7 ) {
    std::cout << "USAGE: ./drawPhotonJet [data_dataset] [mc_dataset] [recoType] [jetAlgo] [FIT_RMS] [flags=\"\"]" << std::endl;
    exit(23);
  }

  std::string data_dataset( argv[1] );
  std::string mc_dataset( argv[2] );
  std::string recoType( argv[3] );
  std::string jetAlgo( argv[4] );
  std::string FIT_RMS( argv[5] );
  std::string flags = "";
  if( argc==7 ) {
    std::string flags_str(argv[6]);
    flags = flags_str;
  }


  std::string algoType;
  if( recoType=="calo" )
    algoType = jetAlgo;
  else
    algoType = recoType+jetAlgo;
  if( recoType=="jpt" && jetAlgo=="akt5") algoType = "jptak5";
  


  DrawExtrap* db = new DrawExtrap("PhotonJet", recoType, jetAlgo);
  db->set_pdf_aussi((bool)false);

  db->set_FITRMS(FIT_RMS);

  char outputdir_char[200];
  if( flags!="" ) {
    sprintf( outputdir_char, "PhotonJetExtrapPlots_%s_vs_%s_%s_%s_%s", data_dataset.c_str(), mc_dataset.c_str(), algoType.c_str(), flags.c_str(), FIT_RMS.c_str());
  } else {
    sprintf( outputdir_char, "PhotonJetExtrapPlots_%s_vs_%s_%s_%s", data_dataset.c_str(), mc_dataset.c_str(), algoType.c_str(), FIT_RMS.c_str());
  }
  std::string outputdir_str(outputdir_char);

  std::vector< float > ptPhot_binning = fitTools::getPtPhot_binning();

  db->set_outputdir(outputdir_str);

  char dataFileName[150];
  if( flags != "" ) {
    sprintf( dataFileName, "PhotonJet_%s_%s_%s.root", data_dataset.c_str(), algoType.c_str(), flags.c_str());
  } else {
    sprintf( dataFileName, "PhotonJet_%s_%s.root", data_dataset.c_str(), algoType.c_str());
  }
  TFile* dataFile = TFile::Open(dataFileName);
  std::cout << "Opened data file '" << dataFileName << "'." << std::endl;

  db->add_dataFile( dataFile, "EG_3pb" );


  char mcFileName[150];
  if( flags!="" && flags!="GENJETS" ) {
    sprintf( mcFileName, "PhotonJet_%s_%s_%s.root", mc_dataset.c_str(), algoType.c_str(), flags.c_str());
  } else {
    sprintf( mcFileName, "PhotonJet_%s_%s.root", mc_dataset.c_str(), algoType.c_str());
  }
  TFile* mcFile = TFile::Open(mcFileName);
  std::cout << "Opened mc file '" << mcFileName << "'." << std::endl;

  db->add_mcFile( mcFile, mc_dataset.c_str(), "#gamma+jet + QCD MC", 46);


  db->set_shapeNormalization();


  bool log = true;

 
  db->drawResponseExtrap();


  delete db;
  db = 0;

  return 0;

}  

