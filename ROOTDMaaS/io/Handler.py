from ROOT import gInterpreter


#required c header for i/o
CHeaders =  'extern "C"\n'
CHeaders += '{\n'
CHeaders += '  #include<string.h>\n'
CHeaders += '  #include <stdio.h>\n'
CHeaders += '  #include <stdlib.h>\n'
CHeaders += '  #include <unistd.h>\n'
CHeaders += '  #include<fcntl.h>\n'
CHeaders += '}\n'


#required class to capture i/o
CPPIOClass ='class ROOTDMSaaSExecutorHandler{'
CPPIOClass +='private:'
CPPIOClass +='  bool capturing;'
CPPIOClass +='  static const unsigned int MAX_LEN=40;'
CPPIOClass +='  Bool_t fStatus=kFALSE;'
#CPPIOClass +='  //this values are to capture stdout, stderr'
CPPIOClass +='  std::string    stdoutpipe;'
CPPIOClass +='  std::string    stderrpipe;'
CPPIOClass +='  char buffer[MAX_LEN];'
CPPIOClass +='  int stdout_pipe[2];'
CPPIOClass +='  int stderr_pipe[2];'
CPPIOClass +='  int saved_stderr;'
CPPIOClass +='  int saved_stdout;'
CPPIOClass +='public:'
CPPIOClass +='ROOTDMSaaSExecutorHandler(){'
CPPIOClass +='  capturing=false;'
CPPIOClass +='}'
CPPIOClass +='void InitCapture()'
CPPIOClass +='{'
CPPIOClass +='  if(!capturing)'
CPPIOClass +='  {'
CPPIOClass +='          saved_stdout = dup(STDOUT_FILENO);'
CPPIOClass +='          saved_stderr = dup(STDERR_FILENO);'
CPPIOClass +='          if( pipe(stdout_pipe) != 0 ) {    '
CPPIOClass +='                  return;'
CPPIOClass +='          }'
CPPIOClass +='          if( pipe(stderr_pipe) != 0 ) {    '
CPPIOClass +='                  return;'
CPPIOClass +='          }'
CPPIOClass +='          long flags_stdout = fcntl(stdout_pipe[0], F_GETFL);'
CPPIOClass +='          flags_stdout |= O_NONBLOCK;'
CPPIOClass +='          fcntl(stdout_pipe[0], F_SETFL, flags_stdout);'
CPPIOClass +='          long flags_stderr = fcntl(stderr_pipe[0], F_GETFL);'
CPPIOClass +='          flags_stderr |= O_NONBLOCK;'
CPPIOClass +='          fcntl(stderr_pipe[0], F_SETFL, flags_stderr);'
CPPIOClass +='          dup2(stdout_pipe[1], STDOUT_FILENO);   '
CPPIOClass +='          close(stdout_pipe[1]);'
CPPIOClass +='          dup2(stderr_pipe[1], STDERR_FILENO);   '
CPPIOClass +='          close(stderr_pipe[1]);'
CPPIOClass +='          capturing = true;'
CPPIOClass +='  }'
CPPIOClass +='}'
CPPIOClass +='void EndCapture()'
CPPIOClass +='{'
CPPIOClass +='  if(capturing)'
CPPIOClass +='  {'
CPPIOClass +='          int buf_readed;'
CPPIOClass +='          while(true)'
CPPIOClass +='          {'
CPPIOClass +='                  fflush(stdout);'
CPPIOClass +='                  buf_readed = read(stdout_pipe[0], buffer, MAX_LEN);'
CPPIOClass +='                  if(buf_readed<=0) break;'
CPPIOClass +='                  for(int i=0;i<buf_readed;i++) stdoutpipe += buffer[i];'
CPPIOClass +='                  memset(buffer,0,MAX_LEN);'
CPPIOClass +='          }'
CPPIOClass +='          while(true)'
CPPIOClass +='          {'
CPPIOClass +='                  fflush(stderr);'
CPPIOClass +='                  buf_readed = read(stderr_pipe[0], buffer, MAX_LEN);'
CPPIOClass +='                  if(buf_readed<=0) break;'
CPPIOClass +='                  for(int i=0;i<buf_readed;i++) stderrpipe += buffer[i];'
CPPIOClass +='                  memset(buffer,0,MAX_LEN);'
CPPIOClass +='          }'
CPPIOClass +='          dup2(saved_stdout, STDOUT_FILENO);  '
CPPIOClass +='          dup2(saved_stderr, STDERR_FILENO);  '
CPPIOClass +='          capturing = false;'
CPPIOClass +='  }'
CPPIOClass +='}'
CPPIOClass +='std::string getStdout(){'
CPPIOClass +='  return stdoutpipe;'
CPPIOClass +='}'
CPPIOClass +='std::string getStderr(){'
CPPIOClass +='  return stderrpipe;'
CPPIOClass +='}'
CPPIOClass +='void clear(){'
CPPIOClass +='  stdoutpipe="";'
CPPIOClass +='  stderrpipe="";'
CPPIOClass +='}'
CPPIOClass +='};'


#function to execute capturing segfault
CPPIOFunctions ='Bool_t ROOTDMaaSExecutor(TString code)'
CPPIOFunctions +='{'
CPPIOFunctions +='  Bool_t status=kFALSE;'
CPPIOFunctions +='  TRY {'
CPPIOFunctions +='    if(gInterpreter->ProcessLine(code.Data()))'
CPPIOFunctions +='    {'
CPPIOFunctions +='      status=kTRUE;'
CPPIOFunctions +='    }'
CPPIOFunctions +='  } CATCH(excode) {'
CPPIOFunctions +='    status=kTRUE;'
CPPIOFunctions +='  } ENDTRY;'
CPPIOFunctions +='  return status;'
CPPIOFunctions +='}'


#function to declare capturing segfault
CPPIOFunctions +='Bool_t ROOTDMaaSDeclarer(TString code)'
CPPIOFunctions +='{'
CPPIOFunctions +='  Bool_t status=kFALSE;'
CPPIOFunctions +='  TRY {'
CPPIOFunctions +='    if(gInterpreter->Declare(code.Data()))'
CPPIOFunctions +='    {'
CPPIOFunctions +='      status=kTRUE;'
CPPIOFunctions +='    }'
CPPIOFunctions +='  } CATCH(excode) {'
CPPIOFunctions +='    status=kTRUE;'
CPPIOFunctions +='  } ENDTRY;'
CPPIOFunctions +='  return status;'
CPPIOFunctions +='}'

def _LoadHeaders():
    gInterpreter.ProcessLine("#include<TRint.h>")
    gInterpreter.ProcessLine("#include<TApplication.h>")
    gInterpreter.ProcessLine("#include<TException.h>")
    gInterpreter.ProcessLine("#include<TInterpreter.h>")
    gInterpreter.ProcessLine("#include <TROOT.h>")
    gInterpreter.ProcessLine("#include<string>")
    gInterpreter.ProcessLine("#include<sstream>")
    gInterpreter.ProcessLine("#include<iostream>")
    gInterpreter.ProcessLine("#include<fstream>")    
    gInterpreter.ProcessLine(CHeaders)

def _LoadClass():
    gInterpreter.Declare(CPPIOClass)


def _LoadFunctions():
    gInterpreter.Declare(CPPIOFunctions)
    
def LoadHandlers():
    _LoadHeaders()
    _LoadClass()
    _LoadFunctions()
