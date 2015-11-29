require(evaluate)

#no me genera el pdf, y me genera el png deseado!
.JuPyROOTRstdout = function(msg){write(msg, stdout())}
.JuPyROOTRstderr = function(msg){write(msg, stderr())}
.plot_files = c()
assign(".plot_files", c(), envir = .GlobalEnv)
.JuPyROOTRPlotHandler = function(obj)
{
tmpfile=tempfile(tmpdir=".",fileext=".png")
png(tmpfile)
replayPlot(obj)
dev.off()
.plot_files = get('.plot_files', envir=.GlobalEnv)
.plot_files = append(.plot_files,tmpfile)
assign(".plot_files", .plot_files, envir = .GlobalEnv)
}


.JuPyROOTROutPutHandler  = new_output_handler(text=.JuPyROOTRstdout,error=.JuPyROOTRstderr,graphics=.JuPyROOTRPlotHandler)

.JuPyROOTRPrintValues = function(x){

classes = evaluate:::classes(x)
len = length(x)-1
for(i in 1:len){
    if(classes[i]=='character') write(x[[i]],stdout())
}
}
.JuPyROOTREvaluate = function(code){
.a=evaluate("options(device=pdf)",new_device=0, envir = .GlobalEnv)
.b=evaluate(code,output_handler = .JuPyROOTROutPutHandler,envir = .GlobalEnv)
.JuPyROOTRPrintValues(.b)
}

# 
# code = 'library(lattice) \n'
# code = paste(code,'attach(mtcars) \n')
# code = paste(code,'gear.f<-factor(gear,levels=c(3,4,5),labels=c("3gears","4gears","5gears")) \n')
# code = paste(code,'cyl.f <-factor(cyl,levels=c(4,6,8),labels=c("4cyl","6cyl","8cyl")) \n')
# code = paste(code,'densityplot(~mpg,main="Density Plot", xlab="Miles per Gallon")\n')


# .ROOTDMaaSREvaluate("2+3")

# .ROOTDMaaSREvaluate("plot(sin)")
# .ROOTDMaaSREvaluate("plot(sin)\nplot(cos)")

# .ROOTDMaaSREvaluate(code)

# a=evaluate("p=recordPlot()")
# a=evaluate("dev.off()")
# tmpfile=tempfile(tmpdir=".",fileext=".png")
# a=evaluate("png('test.png')")#aqui le digo el archivo tempfile
# a=evaluate("replayPlot(p)")
# a=evaluate("dev.off()")

#error para capturar stderr y enviarlo
# result=tryCatch({a=evaluate("d-")},error = function(e){return(e)})
# plot(sin)
# dev.new()
# plot(cos)

# devs=dev.list()
# for (i in devs)
# {
# dev.set(i)
# dev.flush()
# dev.copy(png,tmpfile)
# dev.off()
# }
