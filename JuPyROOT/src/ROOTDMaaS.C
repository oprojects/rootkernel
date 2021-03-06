// @(#)rootkernel$Id$
// Authors: Omar Zapata 2015 ROOT+Jupyter+Kernel project
// Email: Omar.Zapata@cern.ch
// Website: http://oproject.org/ROOT+Jupyter+Kernel

#include<TRint.h>
#include<TApplication.h>
#include<TException.h>
#include<TInterpreter.h>
#include <TROOT.h>

#include<string>
#include<sstream>
#include<iostream>
#include<fstream>

extern "C"
{
  #include<string.h>  
  #include <stdio.h>
  #include <stdlib.h>
  #include <unistd.h>//only for unix
  #include<fcntl.h>//only for unix
}


#ifndef F_LINUX_SPECIFIC_BASE
#define F_LINUX_SPECIFIC_BASE       1024
#endif
#ifndef F_SETPIPE_SZ
#define F_SETPIPE_SZ	(F_LINUX_SPECIFIC_BASE + 7)
#endif

//class to capture stderr/stdout 
//also return the status of the execution
//NOTE: create a system to flush current pipe in a fork
class ROOTDMSaaSExecutorHandler
{
private:
  bool capturing;
  static const unsigned int MAX_LEN=100;
  long MAX_PIPE_SIZE=1048575;
  Bool_t fStatus=kFALSE;    
  
  //this values are to capture stdout, stderr
  std::string    stdoutpipe;
  std::string    stderrpipe;
  char buffer[MAX_LEN];
  int stdout_pipe[2];
  int stderr_pipe[2];
  int saved_stderr;
  int saved_stdout;

public:
  ROOTDMSaaSExecutorHandler(){
    capturing=false;
    std::ios::sync_with_stdio();
    setvbuf( stdout, NULL, _IONBF, 0 );// absolutely needed(flush not needed ;))
    setvbuf( stderr, NULL, _IONBF, 0 );// absolutely needed
  }        
  void InitCapture()
  {
    if(!capturing)
    {
      fflush( stdout );
      /* save stdout/stderr for display later */
      saved_stdout = dup(STDOUT_FILENO);  
      saved_stderr = dup(STDERR_FILENO);  
      if( pipe(stdout_pipe) != 0 ) {          /* make a pipe for stdout*/
        return;
      }
      if( pipe(stderr_pipe) != 0 ) {          /* make a pipe for stderr*/
        return;
      }
      
      long flags_stdout = fcntl(stdout_pipe[0], F_GETFL); 
      flags_stdout |= O_NONBLOCK; 
      fcntl(stdout_pipe[0], F_SETFL, flags_stdout);
      fcntl(stdout_pipe[0], F_SETPIPE_SZ, MAX_PIPE_SIZE);//setting pipe size
     
      long flags_stderr = fcntl(stderr_pipe[0], F_GETFL); 
      flags_stderr |= O_NONBLOCK; 
      fcntl(stderr_pipe[0], F_SETFL, flags_stderr);
      fcntl(stderr_pipe[0], F_SETPIPE_SZ, MAX_PIPE_SIZE);//setting pipe size
      
      dup2(stdout_pipe[1], STDOUT_FILENO);   /* redirect stdout to the pipe */
      close(stdout_pipe[1]);
      
      dup2(stderr_pipe[1], STDERR_FILENO);   /* redirect stderr to the pipe */
      close(stderr_pipe[1]);
      
      
      capturing = true;
    }
  }
  
  void EndCapture()
  {
    if(capturing)
    {
      int buf_readed;
      char ch;
      while(true)/* read from pipe into buffer */
      {
         fflush(stdout);
        buf_readed = read(stdout_pipe[0], &ch, 1);
        if(buf_readed==1) stdoutpipe += ch;
        else break;
      }
      
      while(true)/* read from pipe into buffer */
      {
         fflush(stderr);
        buf_readed = read(stderr_pipe[0], &ch, 1);
        if(buf_readed==1) stderrpipe += ch;
        else break;
      }
      
      
      dup2(saved_stdout, STDOUT_FILENO);  /* reconnect stdout*/
      dup2(saved_stderr, STDERR_FILENO);  /* reconnect stderr*/
      capturing = false;
    }
  }
  
  std::string getStdout()
  {
    return stdoutpipe;
  }
  
  std::string getStderr()
  {
    return stderrpipe;
  }
  
  void clear(){
    stdoutpipe="";
    stderrpipe="";
  }  
};



//function to execute capturing segfault
Bool_t ROOTDMaaSExecutor(TString code)
{
  Bool_t status=kFALSE;
  TRY {
    if(gInterpreter->ProcessLine(code.Data()))
    {
      status=kTRUE;
    }
  } CATCH(excode) {
    status=kTRUE;
  } ENDTRY;
  return status;
}


//function to declare capturing segfault
Bool_t ROOTDMaaSDeclarer(TString code)
{
  Bool_t status=kFALSE;
  TRY {
    if(gInterpreter->Declare(code.Data()))
    {
      status=kTRUE;
    }
  } CATCH(excode) {
    status=kTRUE;
  } ENDTRY;
  return status;
}


Bool_t ROOTDMaaSExecutorR(TString code)
{
  Bool_t status=kFALSE;
  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();
  TRY {
    r.Execute(code);
    status=kTRUE;
  } CATCH(excode) {
    status=kTRUE;
  } ENDTRY;
  return status;
}

std::vector<std::string> ROOTDMaaSExecutorRPlots()
{
  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();
  std::vector<std::string> plots;
  r[".files"]>>plots;
  return plots;
}

std::vector<std::string> ROOTDMaaSExecutorRCompleter(TString code)
{
  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();
  r[".line"]<<code;
  r[".cursor_pos"]<<code.Length();
  
  r<<"utils:::.assignLinebuffer(.line)";
  r<<"utils:::.assignEnd(.cursor_pos)";
  r<<"utils:::.guessTokenFromLine()";
  r<<"utils:::.completeToken()";
  std::vector<std::string> completions;
  int size;
  r["length(utils:::.retrieveCompletions())"]>>size;
  if(size>0) r["utils:::.retrieveCompletions()"]>>completions;
  r<<"utils:::.guessTokenFromLine(update = FALSE)";
  return completions;
}



void ROOTDMaaS()
{
  ROOTDMSaaSExecutorHandler io;
//   io.clear();
//   io.InitCapture();
//    ROOTDMaaSExecutor("int *a=0;");
//    ROOTDMaaSExecutor("a[10]=0;");
//  ROOTDMaaSExecutor("for(int i=0;i<10;i++) std::cout<<i<<std::endl;");
//   ROOTDMaaSExecutorR("print('Hola R')");
//   io.EndCapture();
//   std::cout<<"--------------STDOUT--------------------\n";
//   std::cout<<io.getStdout();
//   std::cout<<"\n--------------STDOUT--------------------\n";
//   std::cout<<io.getStderr();
   
  std::cout<<"\n--------------Completer--------------------\n";
  std::vector<std::string> lines=ROOTDMaaSExecutorRCompleter("read");
 
  for(int i=0;i<lines.size();i++)
  {
      std::cout<<lines[i]<<std::endl;
  }
  lines=ROOTDMaaSExecutorRCompleter("plo");
  std::cout<<"\n--------------Completer--------------------\n";

  for(int i=0;i<lines.size();i++)
  {
      std::cout<<lines[i]<<std::endl;
  }
    
}
