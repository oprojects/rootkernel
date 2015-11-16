// @(#)rootkernel$Id$
// Authors: Omar Zapata, Danilo Piparo, Enric Tejedor 2015 ROOTDMaaS project
// Email: Omar.Zapata@cern.ch
// Website: http://oproject.org/ROOTDMaaS

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


//class to capture stderr/stdout 
//also return the status of the execution
class ROOTDMSaaSExecutorHandler
{
private:
  bool capturing;
  static const unsigned int MAX_LEN=40;
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
  }        
  void InitCapture()
  {
    if(!capturing)
    {
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
      
      long flags_stderr = fcntl(stderr_pipe[0], F_GETFL); 
      flags_stderr |= O_NONBLOCK; 
      fcntl(stderr_pipe[0], F_SETFL, flags_stderr);
      
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
      
      while(true)/* read from pipe into buffer */
      {
        fflush(stdout);
        buf_readed = read(stdout_pipe[0], buffer, MAX_LEN);
        if(buf_readed<=0) break;
        for(int i=0;i<buf_readed;i++) stdoutpipe += buffer[i];
        memset(buffer,0,MAX_LEN);
      }
      
      while(true)/* read from pipe into buffer */
      {
        fflush(stderr);
        buf_readed = read(stderr_pipe[0], buffer, MAX_LEN);
        if(buf_readed<=0) break;
        for(int i=0;i<buf_readed;i++) stderrpipe += buffer[i];
        memset(buffer,0,MAX_LEN);
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

void ROOTDMaaS()
{
  ROOTDMSaaSExecutorHandler io;
  io.clear();
  io.InitCapture();
  ROOTDMaaSExecutor("int *a=0;");
  ROOTDMaaSExecutor("a[10]=0;");
  io.EndCapture();
  std::cout<<"--------------STDOUT--------------------\n";
  std::cout<<io.getStdout();
  std::cout<<"\n--------------STDOUT--------------------\n";
  std::cout<<io.getStderr();
}