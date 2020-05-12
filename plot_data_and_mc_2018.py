# First you will need to import some modules
import ROOT as rt
import functions as f 
import CMS_Lumi
from ROOT import *
import numpy as np
 
# Plots won't pop up during creation
rt.gROOT.SetBatch(rt.kTRUE)

# Variable list and definition of x-axis ranges
variable_list = [  "pt_1", "pt_2", "m_vis", "m_sv" , "njets" , "jpt_1" , "jpt_2" , "mjj" ,"nbtag" , "mTdileptonMET"]
axis_range = {"pt_1" : [20,10,150], "pt_2" : [20,10,150] , "m_vis": [20,30,100], "m_sv": [20,30,200], "njets":[10,0,10] , "jpt_1":[20,30,150], "jpt_2":[20,30,150], "mjj":[20,30,500], "nbtag":[5,0,5] , "mTdileptonMET": [10,0,60]}
title_xaxis = { "pt_1" : "P_{T,e} (GeV)" , "pt_2" : "P_{T,2} (GeV)", "m_vis": "m_{vis} (GeV)" ,"m_sv": "m_{sv} (GeV)" , "njets" : "njets", "jpt_1" : "jpt_{1},(GeV)" , "jpt_2": "jpt_{2}, (GeV)", "mjj" : "m_{jj} , (GeV)", "nbtag":" nbtags" , "mTdileptonMET": "mTdileptonMET(GeV)"}

embedded = True

# Open trees
#input_dir = "/nfs/dust/cms/user/mameyer/SM_HiggsTauTau/HTauTau_emu/Inputs/NTuples_2018"
#input_dir = "/nfs/dust/cms/user/mameyer/SM_HiggsTauTau/HTauTau_emu/Inputs/NTuples_v2_2018"
#input_dir = "/nfs/dust/cms/user/mameyer/SM_HiggsTauTau/HTauTau_emu/Inputs/NTuples_2018"
input_dir = "/nfs/dust/cms/user/mameyer/SM_HiggsTauTau/HTauTau_emu/Inputs/NTuples_2018"
f0,tree_Data   = f.openTree(input_dir+"/em-NOMINAL_ntuple_MuonEG.root","TauCheck")
f1,tree_DYJets = f.openTree(input_dir+"/em-NOMINAL_ntuple_DYJets.root","TauCheck")
f2,tree_SingleTop = f.openTree(input_dir+"/em-NOMINAL_ntuple_SingleTop.root","TauCheck")
f3,tree_TTbar = f.openTree(input_dir+"/em-NOMINAL_ntuple_TTbar.root","TauCheck")
f4,tree_WJets = f.openTree(input_dir+"/em-NOMINAL_ntuple_WJets.root","TauCheck")
f5,tree_Diboson = f.openTree(input_dir+"/em-NOMINAL_ntuple_Diboson.root","TauCheck")
f6,tree_QCD = f.openTree(input_dir+"/em-NOMINAL_ntuple_MuonEG.root","TauCheck")   
f7,tree_ggh = f.openTree(input_dir+"/em-NOMINAL_ntuple_ggH.root","TauCheck")
f8,tree_VBF =  f.openTree(input_dir+"/em-NOMINAL_ntuple_VBFH.root","TauCheck") 
f9,tree_ZTTEM = f.openTree(input_dir+"/em-NOMINAL_ntuple_Embedded.root","TauCheck")

# Definition of  selection
selection = "pt_2>15 && pt_1>15 && iso_1<0.15 && iso_2<0.2  && TMath::Max(pt_1,pt_2)>24 && metFilters && trg_muonelectron &&  mTdileptonMET<60 && extraelec_veto<0.5 && extramuon_veto<0.5 && q_1*q_2 < 0 && nbtag==0 "
     
selection_samesign=  "pt_2>15 && pt_1>15 && iso_1<0.15 && iso_2<0.2  && TMath::Max(pt_1,pt_2)>24 && metFilters && trg_muonelectron &&  mTdileptonMET<60 && extraelec_veto<0.5 && extramuon_veto<0.5 && q_1*q_2 > 0 && nbtag==0  " 

# Definition of weights to be applied

weight = "xsec_lumi_weight*mcweight*puweight*effweight*trigger_filter_weight"
weight_ZTTEM = "mcweight*effweight*embeddedWeight*embedded_stitching_weight*embedded_rate_weight"
weight_TT = weight + "*topptweightRun2"
weight_ZLL = weight + "*zptmassweight"
weight_ZTT = weight + "*zptmassweight"
weight_QCD = "qcdweightml"
weight_ggh = weight+ "*weight_ggh_NNLOPS"
weight_VBF = weight + "*prefiringweight"
    

  
# Create canvas
c = f.createCanvas()
c.SetWindowSize(1000,1000)
c.cd()

#logY = True

for var in variable_list :
  
    # Get x-axis ranges
    nbins , xmin , xmax = axis_range.get(var,[50,0,250])
   
    # Create histograms
    h_Data = f.createH1(var,nbins,xmin,xmax)
    h_ZTT  = h_Data.Clone( "h_ZTT_"+var)
    h_ZLL  = h_Data.Clone( "h_ZLL_"+var)
    h_ST  = h_Data.Clone( "h_ST_"+var)
    h_TTbar  = h_Data.Clone( "h_TTbar_"+var)
    h_WJets  = h_Data.Clone( "h_WJets_"+var)
    h_Diboson  = h_Data.Clone( "h_Diboson_"+var)
    h_QCD  = h_Data.Clone( "h_QCD_"+var)
    h_ggh = h_Data.Clone( "h_ggh_" +var)
    h_VBF = h_Data.Clone("h_VBF_" +var)
    h_ZTTEM = h_Data.Clone("h_ZTTEM_"+var)
    
    # Specify a few settings
    h_Data = f.InitHist(h_Data, var, 1);
    h_ZTT  = f.InitHist(h_ZTT , var, rt.TColor.GetColor("#FFCC66"));
    h_ZLL = f.InitHist(h_ZLL , var ,rt.TColor.GetColor("#9166ff"));
    h_ST   = f.InitHist(h_ST  , var, rt.TColor.GetColor("#FF8766"));
    h_TTbar   = f.InitHist(h_TTbar  , var, rt.TColor.GetColor("#66FFE8"));
    h_WJets   = f.InitHist(h_WJets  , var, rt.TColor.GetColor("#FF66A6"));
    h_Diboson   = f.InitHist(h_Diboson  , var, rt.TColor.GetColor("#BDFF66"));
    h_QCD   = f.InitHist(h_QCD  , var, rt.TColor.GetColor("#EDB2FF"))
    h_ggh   = f.InitHist(h_ggh  , var, rt.TColor.GetColor("#1d2ab8"))
    h_VBF   = f.InitHist(h_VBF  , var, rt.TColor.GetColor("#d92121"));
    h_ZTTEM = f.InitHist(h_ZTTEM,var, rt.TColor.GetColor("#f5ff66"));

    # Draw events from tree to histogram according to defined selection

    tree_Data.Draw(   var + " >> "+h_Data.GetName(), "("+selection+")")
    tree_DYJets.Draw( var + " >> h_ZLL_"+var       , weight_ZLL+"*("+selection+" && isZLL)" )
    tree_SingleTop.Draw( var + " >> h_ST_"+var       , weight+"*("+selection+" ) " )
   
    if embedded:
        tree_TTbar.Draw( var + " >> h_TTbar_"+var       , weight_TT+"*("+selection+" &&!isZTTEM ) " )
        tree_Diboson.Draw( var + " >> h_Diboson_"+var       , weight+"*("+selection+" &&!isZTTEM ) " )
        tree_ZTTEM.Draw(var+ ">>h_ZTTEM_"+var           ,weight_ZTTEM+"*("+selection+" && mcweight<1) "   )
    else:
        tree_DYJets.Draw( var + " >> h_ZTT_"+var       , weight_ZTT +"*("+selection+" && isZTT)" )
        tree_TTbar.Draw( var + " >> h_TTbar_"+var       , weight_TT+"*("+selection+" ) " )
        tree_Diboson.Draw( var + " >> h_Diboson_"+var       , weight+"*("+selection+" ) " )
        
    tree_Data.Draw( var + " >> h_QCD_"+var           , weight_QCD+"*("+selection_samesign+" ) " )
    tree_ggh.Draw( var + " >> h_ggh_"+var           , weight_ggh+"*("+selection+" ) " )
    tree_VBF.Draw( var + " >> h_VBF_"+var           , weight_VBF+"*("+selection+" ) " )
    tree_WJets.Draw( var + " >> h_WJets_"+var       , weight+"*("+selection+" ) " )
    ############################################################################################
    # # Needed for QCD estimation
    h_ZTT_ss  = h_Data.Clone( "h_ZTT_ss"+var)
    h_ZLL_ss  = h_Data.Clone( "h_ZLL_ss"+var)
    h_ST_ss  = h_Data.Clone( "h_ST_ss"+var)
    h_TTbar_ss  = h_Data.Clone( "h_TTbar_ss"+var)
    h_WJets_ss  = h_Data.Clone( "h_WJets_ss"+var)
    h_Diboson_ss  = h_Data.Clone( "h_Diboson_ss"+var)
    h_ZTTEM_ss = h_Data.Clone("h_ZTTEM_ss"+var)

    tree_DYJets.Draw( var + " >> h_ZLL_ss"+var       , weight_ZLL+"*qcdweightml*("+selection_samesign+" && isZLL)" )
    tree_SingleTop.Draw( var + " >> h_ST_ss"+var       , weight+"*qcdweightml*("+selection_samesign+" ) " )
    
    if embedded:
        tree_TTbar.Draw( var + " >> h_TTbar_ss"+var       , weight_TT+"*qcdweightml*("+selection_samesign+" && !isZTTEM ) " )
        tree_Diboson.Draw( var + " >> h_Diboson_ss"+var       , weight+"*qcdweightml*("+selection_samesign+" && !isZTTEM ) " )
        tree_ZTTEM.Draw(var+ ">>h_ZTTEM_ss"+var           ,weight_ZTTEM+"*qcdweightml*("+selection_samesign+" && mcweight<1)")
    else:
        tree_DYJets.Draw( var + " >> h_ZTT_ss"+var       , weight_ZTT +"*qcdweightml*("+selection_samesign+" && isZTT)" )
        tree_TTbar.Draw( var + " >> h_TTbar_ss"+var       , weight_TT+"*qcdweightml*("+selection_samesign+" )" )
        tree_Diboson.Draw( var + " >> h_Diboson_ss"+var       , weight+"*qcdweightml*("+selection_samesign+" ) " )
   
 
    tree_WJets.Draw( var + " >> h_WJets_ss"+var       , weight+"*qcdweightml*("+selection_samesign+" ) " )
    
    
    
    if not embedded: 
        h_QCD.Add(h_ZTT_ss,-1)
        h_QCD.Add(h_ZLL_ss,-1)
        h_QCD.Add(h_ST_ss,-1)
        h_QCD.Add(h_TTbar_ss,-1)
        h_QCD.Add(h_WJets_ss,-1)
        h_QCD.Add(h_Diboson_ss,-1)
    else:
        h_QCD.Add(h_ZTTEM_ss,-1)
        h_QCD.Add(h_ZLL_ss,-1)
        h_QCD.Add(h_ST_ss,-1)
        h_QCD.Add(h_WJets_ss,-1)
        h_QCD.Add(h_Diboson_ss,-1)
        h_QCD.Add(h_TTbar_ss,-1)

    ############################################################################################


    
    print "data = " + str(h_Data.GetSumOfWeights() )
    print "ZTT  = " + str(h_ZTT.GetSumOfWeights() )
    print "ZLL  = " + str(h_ZLL.GetSumOfWeights() )
    print "ST  = " + str(h_ST.GetSumOfWeights()  )
    print "TTbar   = " + str(h_TTbar.GetSumOfWeights()  )
    print "WJets  = " + str(h_WJets.GetSumOfWeights()  )
    print "Diboson  = " + str(h_Diboson.GetSumOfWeights()  )
    print "QCD    = " + str(h_QCD.GetSumOfWeights()  )
    print "ggh    = " + str(h_ggh.GetSumOfWeights()  )
    print "VBF    = " + str(h_VBF.GetSumOfWeights()  )
    print "ZTTEM = " + str (h_ZTTEM.GetSumOfWeights() )
   
    if embedded:
        
           print "Bkg  = " + str(h_ST.GetSumOfWeights()+h_TTbar.GetSumOfWeights()+h_WJets.GetSumOfWeights()+h_Diboson.GetSumOfWeights()+ h_ZLL.GetSumOfWeights() + h_QCD.GetSumOfWeights()+ h_ZTTEM.GetSumOfWeights())
        
    else:
           print "Bkg = " + str(h_ZTT.GetSumOfWeights()+h_ST.GetSumOfWeights()+h_TTbar.GetSumOfWeights()+h_WJets.GetSumOfWeights()+h_Diboson.GetSumOfWeights()+ h_ZLL.GetSumOfWeights() + h_QCD.GetSumOfWeights())
    
    
    
    
    
    #General uncertainties
    err_lumi = 0.025;
    err_trigger = 0.020;
    err_muon_eff = 0.014;
    err_elec_eff = 0.014;

   #Sample-specific uncertainties
    err_vv_xsec  = 0.05;
    err_st_xsec  = 0.05;
    err_tt_xsec  = 0.06;
    err_w_xsec   = 0.04;
    err_dy_xsec  = 0.04;
    err_qcd_norm = 0.10;
    err_emb_norm = 0.04;

    if embedded:
        err_norm_general =np.array( [err_trigger , err_muon_eff , err_elec_eff] );
        #print('err_norm_general', err_norm_general)
    else:
        err_norm_general =np.array( [err_lumi, err_trigger , err_muon_eff , err_elec_eff] );
        #print('err_norm_general', err_norm_general)

    # Create a stack with all backgrounds
    bkg = rt.THStack("Background","");
    if not embedded:
        bkg.Add(h_ZTT);
        bkg.Add(h_ZLL);
        bkg.Add(h_ST);
        bkg.Add(h_TTbar);
        bkg.Add(h_WJets);
        bkg.Add(h_Diboson);
        bkg.Add(h_QCD);
    else:
        bkg.Add(h_QCD);
        bkg.Add(h_Diboson);
        bkg.Add(h_ST);
        bkg.Add(h_ZLL);
        bkg.Add(h_WJets);
        bkg.Add(h_TTbar);
        bkg.Add(h_ZTTEM);
        
    #define new Histogram for statistical errors
   
    back_err= bkg.GetStack().Last().Clone("back_err");
    back_err.SetMarkerSize(0);
    back_err.SetFillStyle(3004);
    back_err.SetFillColor(923);
    back_err.SetMarkerSize(0);

    for i in range (1,nbins):
        x = back_err.GetBinContent(i);
        err_stat = back_err.GetBinError(i);
        err_norm_abs = np.array([]);
        z = err_norm_abs
        for err in err_norm_general:
            z= np.append(z,err*x);
            #print('z',z)
          
            
        Y= np.append(z, h_VBF.GetBinContent(i)*err_vv_xsec );
        W=np.append(Y, h_ST.GetBinContent(i)*err_st_xsec );
        Z=np.append(W,  h_TTbar.GetBinContent(i)*err_tt_xsec );
        X=np.append(Z,  h_WJets.GetBinContent(i)*err_w_xsec );
        U=np.append(X,h_ZLL.GetBinContent(i)*err_dy_xsec );
        
        if embedded:
            A=np.append(U,h_ZTTEM.GetBinContent(i)*err_emb_norm );
            S=np.append(A, h_QCD.GetBinContent(i)*err_qcd_norm );
        else:
            V=np.append(X, h_ZTT.GetBinContent(i)*err_dy_xsec );
            S=np.append(V, h_QCD.GetBinContent(i)*err_qcd_norm );
        
       

        err_total = err_stat*err_stat;

        for err_bin in S:
            err_total += err_bin*err_bin;
   
        err_total = np.sqrt(err_total);
        #print('err_total', err_total)
        back_err.SetBinError(i,err_total);



    # Draw the upper pad
    upper_pad = rt.TPad("upper", "pad",0,0.31,1,1)
    upper_pad.cd();
    title = title_xaxis.get(var ," ")
    h_Data.GetXaxis().SetTitle(title);
    h_Data.GetXaxis().SetTitleSize(0.04);
    h_Data.GetXaxis().SetTitleOffset(1.0);
    h_Data.GetYaxis().SetTitle("Events");
    h_Data.GetYaxis().SetTitleOffset(1.95);
    
    #if not logY:
    h_Data.GetYaxis().SetRangeUser(0,h_Data.GetMaximum()*1.2);
    upper_pad.SetBottomMargin(0.10);
    upper_pad.SetLeftMargin(0.10);
    h_ggh.Scale(100)
    h_ggh.SetFillStyle(0)
    h_ggh.SetLineColor(4)
    h_VBF.Scale(100)
    h_VBF.SetFillStyle(0)
    h_VBF.SetLineColor(2)
    h_Data.GetMaximum()*1.2
    print (h_Data.GetMaximum()*1.2)
    h_Data.Draw("e1");
    CMS_Lumi.draw(upper_pad, "2018");
    bkg.Draw("hist same")
    back_err.Draw("e2same")
    h_ggh.Draw ("hist same")
    h_VBF.Draw("hist same")
    h_Data.Draw("pe same")

    # Make a legend to the plot
    legend = rt.TLegend(0.65,0.55,0.90,0.90);
    legend.SetTextFont(42);
    legend.AddEntry(h_Data, "Observed", "ple");
    if not embedded:
        legend.AddEntry(h_ZTT,"Z#rightarrow #tau#tau","f");
    else:
        legend.AddEntry(h_ZTTEM, "Z#rightarrow #tau#tau(emb)","f")
    legend.AddEntry(h_ZLL,"Z#rightarrow ll ","f" );
    legend.AddEntry(h_ST,"SingleTop","f");
    legend.AddEntry(h_TTbar,"TTbar","f" );
    legend.AddEntry(h_WJets,"WJets","f" );
    legend.AddEntry(h_Diboson,"Diboson","f" );
    legend.AddEntry(h_QCD , "QCD","f" );
    legend.AddEntry(h_ggh ,"ggh" , "l" )
    legend.AddEntry(h_VBF,"VBF","l" )
    legend.Draw("same")

    # Make a ratio plot and draw it to lower pad
    lower_pad = rt.TPad("lower", "pad",0,0,1,0.31)
    lower_pad.cd()
    histo_ratio = h_Data.Clone("ratioH");
    histo_ratioErr= back_err.Clone("ratioErrH"); 
    for i in range(1,nbins+1):
        value = histo_ratioErr.GetBinContent(i);
        abs_error = histo_ratioErr.GetBinError(i);
        if value < 0.00001:
            rel_error = 0;
        else:
            rel_error = abs_error/value;
        histo_ratioErr.SetBinError(i,rel_error);
        histo_ratioErr.SetBinContent(i,1);

    histo_ratio = f.InitHist(histo_ratio, var, 1)
    histo_ratio.Divide(bkg.GetStack().Last())
    histo_ratio.GetYaxis().SetRangeUser(0.5,1.5);
    histo_ratio.GetYaxis().SetTitle("Data/Background");
    #histo_ratio.GetXaxis().SetTitle("P_{T}");
    histo_ratio.GetXaxis().SetTitleOffset(1.5);
    histo_ratio.GetXaxis().SetTitleSize(0.045);
    lower_pad.SetLeftMargin(0.10);
    lower_pad.SetTopMargin(0);
    histo_ratio.Draw(" e same")
    histo_ratioErr.Draw("e2 same")
    lower_pad.Update();
    lower_pad.SetBorderSize(2);
   

    #draw a line for ratio 1

    line = rt.TLine (xmin ,1 ,xmax ,1)
    line.SetLineColor(rt.kBlue)
    line.SetLineWidth (2)
    line.Draw("same")
   
    #Draw both pads to canvas
    c.cd()
    #upper_pad.SetLogy(logY);
    #upper_pad.SetLogy()
    upper_pad.Draw("same A")
    lower_pad.Draw("same")
    #lower_pad.SetBorderSize(10

    # Save plot
    if embedded:
        c.Print("figures_controlplots_emb_2018_newNtuples/"+var+".png")    
    else:
        c.Print("figure_controlplots_neue_Ntuple/"+var+".png")   
    # Clean gDirectory
    rt.gDirectory.Delete("h1")
    rt.gDirectory.Delete("h2")
