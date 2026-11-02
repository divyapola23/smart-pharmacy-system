$docxPath = (Resolve-Path ".\SMART_PHARMACY_PROJECT_REPORT.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
Write-Host "Converting $docxPath to $pdfPath..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "Successfully generated PDF: $pdfPath"
} catch {
    Write-Error $_
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
