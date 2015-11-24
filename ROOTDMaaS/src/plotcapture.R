options(device='png')
# require(grDevices)
.files = c()
.dev.new = dev.new
.png = png

assign(".files", c(), envir = .GlobalEnv)
assign(".dev.new",dev.new, envir = .GlobalEnv)
assign(".png",png, envir = .GlobalEnv)

png = function(filename = "Rplot.png",width = 480, height = 480, units = "px", pointsize = 12,bg = "white",  res = NA, ...,type = c("cairo", "cairo-png", "Xlib", "quartz"),antialias)
{
.png = get('.png', envir=.GlobalEnv)
tmpfile=filename
if(filename == "Rplot.png")
{
  tmpfile=tempfile(tmpdir=".",fileext=".png")
}
.png(tmpfile,width,height,units,pointsize,bg,res)
.files = get('.files', envir=.GlobalEnv)
.files = append(.files,tmpfile)
assign(".files", .files, envir = .GlobalEnv)
}

dev.new = function()
{
png()
}

unlockBinding("png",getNamespace("grDevices"))
assign("png", png, getNamespace("grDevices"))
lockBinding("png", getNamespace("grDevices"))

# unlockBinding("termplot", )
# assign("termplot", my.termplot, as.environment("package:stats"))
# lockBinding("termplot", as.environment("package:stats"))
# x11=dev.new
# windows=dev.new

plot(sin)
dev.new()
plot(cos)

for (i in dev.list())
{
dev.set(i)
dev.flush()
dev.off()
}
