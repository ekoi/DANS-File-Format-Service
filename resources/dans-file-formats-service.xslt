<?xml version="1.0"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs math" version="3.0">
    <xsl:output indent="yes" omit-xml-declaration="yes" />
    <xsl:template match="data">
        <!-- create a new root tag -->
        <!-- apply the xml structure generated from JSON -->
        <xsl:apply-templates select="json-to-xml(.)" />
    </xsl:template>
    <!-- template for the first tag -->
    <xsl:template match="/array"
        xpath-default-namespace="http://www.w3.org/2005/xpath-functions">
        {
        <xsl:for-each select="/array/map/array[@key='preferred-format']">
            <xsl:if test="(preceding-sibling::array[@key='type']/map/string[@key='title']='Audio') or (preceding-sibling::array[@key='type']/map/string[@key='title']='Video')">
            <xsl:if test="position() != 1">
                <xsl:text>,</xsl:text>
            </xsl:if>
            <xsl:for-each select="./map/string[@key='file-ext']">
                <xsl:if test="position() != 1">
                    <xsl:text>,</xsl:text>
                </xsl:if>
                "<xsl:value-of select="."/>":{"preferred": "yes"}
            </xsl:for-each>
            </xsl:if>
        </xsl:for-each>
        <xsl:for-each select="/array/map/array[@key='non-preferred-format']">
            <xsl:if test="(preceding-sibling::array[@key='type']/map/string[@key='title']='Audio') or (preceding-sibling::array[@key='type']/map/string[@key='title']='Video')">
            <xsl:for-each select="./map/string[@key='file-ext']">
                ,
                <xsl:choose>
                    <xsl:when test="following-sibling::string[@key='pre-ingest']/text() !=''">
                        "<xsl:value-of select="."/>":{"preferred": "no", "dissemination-conversion":"<xsl:value-of select="following-sibling::string[@key='pre-ingest']/text()"/>", "preservation-conversion":"<xsl:value-of select="following-sibling::string[@key='preservation']/text()"/>"}
                    </xsl:when>
                    <xsl:otherwise>
                        "<xsl:value-of select="."/>":{"preferred": "no", "dissemination-conversion":"no", "preservation-conversion":"<xsl:value-of select="following-sibling::string[@key='preservation']/text()"/>"}
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            </xsl:if>
        </xsl:for-each>
        }

    </xsl:template>
    <xsl:template name="preferred-format"></xsl:template>
    <xsl:template name="non-preferred-format"></xsl:template>
</xsl:stylesheet>