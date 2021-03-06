USE [master]
GO
/****** Object:  Database [SmallWordsEducation]    Script Date: 9.06.2019 18:41:00 ******/
CREATE DATABASE [SmallWordsEducation]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'SmallWordsEducation', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL12.DEVOPSTEAM\MSSQL\DATA\SmallWordsEducation.mdf' , SIZE = 180224KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'SmallWordsEducation_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL12.DEVOPSTEAM\MSSQL\DATA\SmallWordsEducation_log.ldf' , SIZE = 916352KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [SmallWordsEducation] SET COMPATIBILITY_LEVEL = 120
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [SmallWordsEducation].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [SmallWordsEducation] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET ARITHABORT OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [SmallWordsEducation] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [SmallWordsEducation] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [SmallWordsEducation] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET  DISABLE_BROKER 
GO
ALTER DATABASE [SmallWordsEducation] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET ALLOW_SNAPSHOT_ISOLATION ON 
GO
ALTER DATABASE [SmallWordsEducation] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [SmallWordsEducation] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET RECOVERY FULL 
GO
ALTER DATABASE [SmallWordsEducation] SET  MULTI_USER 
GO
ALTER DATABASE [SmallWordsEducation] SET PAGE_VERIFY NONE  
GO
ALTER DATABASE [SmallWordsEducation] SET DB_CHAINING OFF 
GO
ALTER DATABASE [SmallWordsEducation] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [SmallWordsEducation] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO
ALTER DATABASE [SmallWordsEducation] SET DELAYED_DURABILITY = DISABLED 
GO
USE [SmallWordsEducation]
GO
/****** Object:  UserDefinedFunction [dbo].[Factorial]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [dbo].[Factorial] ( @iNumber FLOAT )
RETURNS FLOAT
AS
BEGIN
declare @defaultValue FLOAT=7.25
if @iNumber >170
return @defaultValue
else
       DECLARE @i  FLOAT
	   SELECT @i= ISNULL(EXP(SUM(LOG(N))),1)
	   FROM dbo.Tally
	  WHERE N BETWEEN 1 AND @iNumber;
   RETURN (@i)
END




GO
/****** Object:  UserDefinedFunction [dbo].[Split]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create FUNCTION [dbo].[Split]
(
	@List nvarchar(max),
	@SplitOn nvarchar(5)
)  
RETURNS @RtnValue table 
(
		
	Id int identity(1,1),
	Value nvarchar(100)
) 
AS  
BEGIN

 



While (Charindex(@SplitOn,@List)>0)
Begin  




Insert Into @RtnValue (Value)
Select 
    Value = ltrim(rtrim(Substring(@List,1,Charindex(@SplitOn,@List)-1)))  




    Set @List = Substring(@List,Charindex(@SplitOn,@List)+len(@SplitOn),len(@List))
End  




    Insert Into @RtnValue (Value)
    Select Value = ltrim(rtrim(@List))

    Return
END




GO
/****** Object:  Table [dbo].[Documents]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Documents](
	[Id] [int] NOT NULL,
	[DocumentName] [nvarchar](max) NOT NULL,
	[Topic] [nvarchar](max) NULL,
	[SubTopic] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[DocumentSimilarity]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DocumentSimilarity](
	[DocumentOne] [int] NULL,
	[DocumentOneTopic] [nvarchar](max) NULL,
	[DocumentOneSubTopic] [nvarchar](max) NULL,
	[DocumentTwo] [int] NULL,
	[DocumentTwoTopic] [nvarchar](max) NULL,
	[DocumentTwoSubTopic] [nvarchar](max) NULL,
	[SimilarityResult] [decimal](18, 6) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[DocumentsPMI]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DocumentsPMI](
	[WordOne] [nvarchar](50) NULL,
	[WordOneId] [int] NULL,
	[WordTwo] [nvarchar](50) NULL,
	[WordTwoId] [int] NULL,
	[DocumentId] [int] NULL,
	[PMI] [decimal](18, 10) NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[DocumentVector]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DocumentVector](
	[DocumentId] [int] NOT NULL,
	[Vector] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[EnglishDictionary]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[EnglishDictionary](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Word] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[EnglishDictionaryTemp]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[EnglishDictionaryTemp](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Word] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[MeaningWord]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MeaningWord](
	[DocumentId] [int] NOT NULL,
	[StemWord] [nvarchar](150) NOT NULL,
	[MeaningValue] [decimal](30, 4) NOT NULL,
	[WordId] [int] IDENTITY(0,1) NOT NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[OriginalWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[OriginalWords](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[StemWord] [varchar](100) NULL,
	[OriginalWord] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[ProbabilitiesOfAssociation]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ProbabilitiesOfAssociation](
	[Word1] [nvarchar](50) NULL,
	[Word1Index] [int] NOT NULL,
	[Word2] [nvarchar](50) NULL,
	[Word2Index] [int] NOT NULL,
	[AssociationProp] [decimal](18, 6) NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SearchedDocuments]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SearchedDocuments](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[DocumentName] [nvarchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SingleWordProp]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SingleWordProp](
	[DocumentId] [int] NULL,
	[Word] [nvarchar](50) NULL,
	[Probability] [decimal](18, 6) NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Tally]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tally](
	[N] [int] NOT NULL,
 CONSTRAINT [PK_Tally_N] PRIMARY KEY CLUSTERED 
(
	[N] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[TFIDFWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TFIDFWords](
	[WordID] [int] IDENTITY(1,1) NOT NULL,
	[DocumentId] [int] NULL,
	[Word] [nvarchar](150) NULL,
	[TF] [decimal](30, 4) NULL,
	[IDF] [decimal](30, 4) NULL,
	[TF_IDF] [decimal](30, 4) NULL,
PRIMARY KEY CLUSTERED 
(
	[WordID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Words]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Words](
	[WordID] [int] IDENTITY(1,1) NOT NULL,
	[DocumentId] [int] NULL,
	[Word] [nvarchar](150) NULL,
	[Count] [int] NULL,
	[StemWord] [nvarchar](150) NULL,
	[Paragraph] [int] NULL,
 CONSTRAINT [PK_Words] PRIMARY KEY CLUSTERED 
(
	[WordID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_Word]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_Word] ON [dbo].[EnglishDictionary]
(
	[Word] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_Word_Temp]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_Word_Temp] ON [dbo].[EnglishDictionaryTemp]
(
	[Word] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [IX_MeaningValue]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_MeaningValue] ON [dbo].[MeaningWord]
(
	[MeaningValue] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_StemWord]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_StemWord] ON [dbo].[OriginalWords]
(
	[StemWord] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [IX_DocumentId]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_DocumentId] ON [dbo].[Words]
(
	[DocumentId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_StemWord]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_StemWord] ON [dbo].[Words]
(
	[StemWord] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_StemWord_DocumentId]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_StemWord_DocumentId] ON [dbo].[Words]
(
	[StemWord] ASC,
	[DocumentId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [IX_Word]    Script Date: 9.06.2019 18:41:01 ******/
CREATE NONCLUSTERED INDEX [IX_Word] ON [dbo].[Words]
(
	[Word] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[DeleteWordsForMeaningWordsCalculation]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create proc [dbo].[DeleteWordsForMeaningWordsCalculation] 
@count_Paragraph_Threshold int,
@sum_Count_Threshold int
as 
begin
delete from dbo.Words
where stemword IN(select stemword 
			from Words w (nolock) 
			group by Paragraph,StemWord,DocumentId
			having (select Count(Paragraph) from Words (nolock) 
			where StemWord=w.StemWord and DocumentId=w.DocumentId)>@count_Paragraph_Threshold
			 or (select Sum(Count) from Words (nolock) 
			 where StemWord=w.StemWord and DocumentId=w.DocumentId)>@sum_Count_Threshold)
end
GO
/****** Object:  StoredProcedure [dbo].[GetDistinctWordList]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetDistinctWordList] 
as
begin

select distinct Word from Words(nolock)

end
GO
/****** Object:  StoredProcedure [dbo].[GetDocumentCountOfIncludeTerm]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetDocumentCountOfIncludeTerm]  @word [nvarchar](150)
as
begin

select DocumentId from Words (nolock)
where Word=@word
group by DocumentId 

end

GO
/****** Object:  StoredProcedure [dbo].[GetDocumentIdList]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetDocumentIdList] 
AS 
BEGIN
SELECT Id FROM Documents
  END


GO
/****** Object:  StoredProcedure [dbo].[GetEnglishDictionary]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create proc [dbo].[GetEnglishDictionary]
as 
begin
SELECT Word FROM [SmallWordsEducation].[dbo].[EnglishDictionary]
end
GO
/****** Object:  StoredProcedure [dbo].[GetEnglishDictionaryTemp]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE proc [dbo].[GetEnglishDictionaryTemp]
as 
begin
SELECT top 1 Word FROM [SmallWordsEducation].[dbo].[EnglishDictionaryTemp]
end
GO
/****** Object:  StoredProcedure [dbo].[GetMaxLevelMeaningWord]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE proc [dbo].[GetMaxLevelMeaningWord] @tf decimal(30,4)
as
begin

declare @count int 
SELECT @count=count(*) FROM 
[SmallWordsEducation].[dbo].[SearchedDocuments] (nolock)

if @count>0
begin
select top 1 t.Word from TFIDFWords t (nolock)
 where t.Word not in (select Word from EnglishDictionary)
 AND t.TF>=@tf
order by t.TF desc
end
else 
begin
select top 1 t.Word from TFIDFWords t (nolock)
 where t.Word not in (select Word from EnglishDictionary)
order by t.TF desc
end
end
GO
/****** Object:  StoredProcedure [dbo].[GetMaxTermOnDocument]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create proc [dbo].[GetMaxTermOnDocument] @documentId int
as
begin

select top 1 Word ,sum(count) as [Count] from Words
where DocumentId=@documentId 
group by Word 
order by [Count] desc

end
GO
/****** Object:  StoredProcedure [dbo].[GetMeaningWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create proc [dbo].[GetMeaningWords] @min_MeaningValue decimal(30,4) ,@max_MeaningValue decimal(30,4)
as 
begin
select StemWord from [dbo].[MeaningWord] where MeaningValue 
between @min_MeaningValue and @max_MeaningValue
end
GO
/****** Object:  StoredProcedure [dbo].[GetMeaningWords_TopCount]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[GetMeaningWords_TopCount] @topCount int
as 
begin
select top(@topCount) StemWord from [dbo].[MeaningWord] order by MeaningValue desc
end
GO
/****** Object:  StoredProcedure [dbo].[GetOriginalWord]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetOriginalWord] @word nvarchar(150)
as
begin

select OriginalWord from OriginalWords (nolock)
where StemWord=@word

end
GO
/****** Object:  StoredProcedure [dbo].[GetParameterTopCountMeaningWord]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetParameterTopCountMeaningWord] @topCount int
as
begin

select top (@topCount) Word from TFIDFWords (nolock)
order by TF_IDF desc
end
GO
/****** Object:  StoredProcedure [dbo].[GetTermCountOnDocument]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create proc [dbo].[GetTermCountOnDocument] @documentId int,@word [nvarchar](150)
as
begin

select Word ,sum(count) as deger from Words
where DocumentId=@documentId and Word=@word
group by Word 

end
GO
/****** Object:  StoredProcedure [dbo].[GetTermFrequency]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetTermFrequency] @word [nvarchar](150)
as
begin

select sum(count) as deger from Words
where Word=@word


end
GO
/****** Object:  StoredProcedure [dbo].[GetTFIDFWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE proc [dbo].[GetTFIDFWords] @tfIDF decimal(30,4)
as
begin

--set @tfIDF =0.02
select  Word from TFIDFWords (nolock)
where TF>=@tfIDF
end
GO
/****** Object:  StoredProcedure [dbo].[GetTFIDFWords_TopCount]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[GetTFIDFWords_TopCount] @topCount int
as 
begin
select top(@topCount) Word from [dbo].TFIDFWords order by TF_IDF desc
end
GO
/****** Object:  StoredProcedure [dbo].[GetTFIDFWordsAverageCalculationResult]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[GetTFIDFWordsAverageCalculationResult]
as 
begin

declare @averageTFRate decimal(30,4)
select @averageTFRate=SUM(A.TF)/10 from  
(
select top 10 TF from TFIDFWords
order by TF desc
)a

select Word from TFIDFWords (nolock)
where TF>=@averageTFRate
ORDER BY TF desc

end

GO
/****** Object:  StoredProcedure [dbo].[GetTotalDocumentCount]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetTotalDocumentCount]
as
begin

select count(1) from Documents(nolock)

end

GO
/****** Object:  StoredProcedure [dbo].[GetTotalPMI]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE proc [dbo].[GetTotalPMI] @topCount int
AS 
BEGIN
SELECT top(@topCount)[WordOne] AS Word
      ,sum([PMI]) AS TotalPMI
  FROM [SmallWordsEducation].[dbo].[DocumentsPMI]
  where WordOne<>WordTwo
  group by WordOne
  order by sum(PMI) desc
  END


GO
/****** Object:  StoredProcedure [dbo].[GetTotalWordsFrequency]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


create proc [dbo].[GetTotalWordsFrequency]
as
begin

select sum(Count) from Words(nolock)

end

GO
/****** Object:  StoredProcedure [dbo].[GetWordListOnDocument]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[GetWordListOnDocument] @documentId int
as
begin

select distinct Word from Words(nolock)
where DocumentId=@documentId

end
GO
/****** Object:  StoredProcedure [dbo].[GetWords_TopCount]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[GetWords_TopCount] @topCount int
as 
begin
select distinct top(@topCount) w.Word  from [dbo].Words as w
inner join EnglishDictionary e on w.Word!=e.Word
end
GO
/****** Object:  StoredProcedure [dbo].[InsertEnglishDictionary]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[InsertEnglishDictionary] @word varchar(max)
as 
begin
if not exists(select top 1 * from [dbo].[EnglishDictionary][Words] where Word=@word)
insert into [dbo].[EnglishDictionary]([Word])
select @word
end
GO
/****** Object:  StoredProcedure [dbo].[InsertEnglishDictionary_TopCount]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
 create proc [dbo].[InsertEnglishDictionary_TopCount] @topCount int 
  as 
  begin 
  insert into [dbo].[EnglishDictionary]([Word])
  select top(@topCount) stemword from [dbo].[MeaningWord] order by MeaningValue desc
  end
GO
/****** Object:  StoredProcedure [dbo].[InsertEnglishDictionaryTemp]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[InsertEnglishDictionaryTemp] @word varchar(max)
as 
begin
if not exists(select top 1 * from [dbo].[EnglishDictionaryTemp][Words] where Word=@word)
insert into [dbo].[EnglishDictionaryTemp]([Word])
select @word
end
GO
/****** Object:  StoredProcedure [dbo].[InsertMeaningValue]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [dbo].[InsertMeaningValue]

AS
BEGIN
		Insert into MeaningWord
		(
			DocumentId,
			StemWord,
			MeaningValue
		)
		Select DocumentId,
			Stemword,
			Cast(LOG(A*B) as decimal)/-M as MV
		From
		(Select DocumentId,
			   StemWord,
			   K,
			   M,
			   Cast((SELECT 1/(SELECT POWER((Select CAST((Select Sum(Count) from Words) AS FLOAT)/(Select Sum(x.TotalWord) From (Select Sum(COUNT) as TotalWord From Words Where Paragraph in ( Select Distinct Paragraph from Words where x.StemWord=StemWord and x.DocumentId=DocumentId) group by Paragraph) as x)),M-1))) as decimal(18,2)) A,
			   (SELECT dbo.Factorial(K)/dbo.Factorial(M)*dbo.Factorial(K-M)) B
		From(
			select distinct DocumentId, StemWord ,
			(select Count(Paragraph) from Words  where StemWord=w.StemWord and DocumentId=w.DocumentId) M,
			(select Sum(Count) from Words where StemWord=w.StemWord and DocumentId=w.DocumentId ) K
			from Words w
			)
		as x
		) as y
		Where A*B>0 and Cast(LOG(A*B) as decimal)/-M>0
		Order By DocumentId,MV desc
		
END
GO
/****** Object:  StoredProcedure [dbo].[InsertOriginalWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[InsertOriginalWords] @StemWord varchar(100),@OriginalWord varchar(100)
as 
begin
if not exists(select top 1 * from OriginalWords where StemWord=@StemWord)
insert into [dbo].OriginalWords(StemWord,OriginalWord)
select @StemWord,@OriginalWord
end
GO
/****** Object:  StoredProcedure [dbo].[InsertSearchedDocuments]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create proc [dbo].[InsertSearchedDocuments]
 @documentName nvarchar(max)
as
begin

Insert into SearchedDocuments
select @documentName

end
GO
/****** Object:  StoredProcedure [dbo].[InsertTally]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


create procedure [dbo].[InsertTally] @count int
as 
begin
DECLARE @i int = 0
WHILE @i < @count 
BEGIN
    SET @i = @i + 1
	insert into Tally
	select @i
end
end

GO
/****** Object:  StoredProcedure [dbo].[InsertTFIDFWords]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[InsertTFIDFWords] @documentId int,@word [nvarchar](150),@tf decimal(30,4),@idf decimal(30,4),@tf_idf decimal(30,4)
as
begin

if not exists(select top 1 * from TFIDFWords(nolock) where [Word]=@word and DocumentId=@documentId)
begin
insert into TFIDFWords
select @documentId,@word,@tf,@idf,@tf_idf
end

end

GO
/****** Object:  StoredProcedure [dbo].[TruncateAllDatabase]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[TruncateAllDatabase]
as
begin
truncate table [SmallWordsEducation].[dbo].[MeaningWord]
truncate table [SmallWordsEducation].[dbo].[Words]
truncate table [SmallWordsEducation].[dbo].[Documents]
--truncate table [SmallWordsEducation].[dbo].[EnglishDictionaryTemp]
--truncate table [SmallWordsEducation].[dbo].[OriginalWords]
truncate table [SmallWordsEducation].[dbo].[TFIDFWords]
truncate table [SmallWordsEducation].[dbo].DocumentVector
truncate table [SmallWordsEducation].[dbo].DocumentsPMI
truncate table [SmallWordsEducation].[dbo].SingleWordProp
truncate table [SmallWordsEducation].[dbo].ProbabilitiesOfAssociation
truncate table [SmallWordsEducation].[dbo].DocumentSimilarity

end
GO
/****** Object:  StoredProcedure [dbo].[TruncateSelectedDatabase]    Script Date: 9.06.2019 18:41:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE proc [dbo].[TruncateSelectedDatabase]
as
begin
truncate table [SmallWordsEducation].[dbo].[MeaningWord]
truncate table [SmallWordsEducation].[dbo].[Tally]
truncate table [SmallWordsEducation].[dbo].[Words]
end
GO
USE [master]
GO
ALTER DATABASE [SmallWordsEducation] SET  READ_WRITE 
GO
