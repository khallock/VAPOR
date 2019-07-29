#ifndef FLOWPARAMS_H
#define FLOWPARAMS_H

#include <vapor/RenderParams.h>
#include <vapor/DataMgr.h>

namespace VAPoR 
{

class PARAMS_API FlowParams : public RenderParams 
{
public:

    FlowParams( DataMgr*                 dataManager, 
                ParamsBase::StateSave*   stateSave );
    FlowParams( DataMgr*                 dataManager, 
                ParamsBase::StateSave*   stateSave, 
                XmlNode*                 xmlNode );

    virtual ~FlowParams();

    //
    // (Pure virtual methods from RenderParams)
    //
    virtual bool IsOpaque() const override
    { 
        return false; 
    }
    virtual bool usingVariable(const std::string& varname) override
    {
        return false;
    }

    static std::string GetClassType() 
    {
        return ("FlowParams");
    }

    // True  == Steady; False == Unteady
    void   SetIsSteady( bool steady );
    bool   GetIsSteady() const;

    double GetVelocityMultiplier() const;
    void   SetVelocityMultiplier( double );

    long   GetSteadyNumOfSteps() const;
    void   SetSteadyNumOfSteps( long );

    long   GetSeedGenMode() const;
    void   SetSeedGenMode( long );

    void   SetNeedFlowlineOutput( bool );
    bool   GetNeedFlowlineOutput( ) const;

    long   GetFlowDirection() const;
    void   SetFlowDirection( long );

    std::string GetSeedInputFilename() const;
    void        SetSeedInputFilename( const std::string& ) ;

    std::string GetFlowlineOutputFilename() const;
    void        SetFlowlineOutputFilename( const std::string& ) ;

    std::vector<bool>   GetPeriodic() const;
    void                SetPeriodic( const std::vector<bool>& );

    // 6 values to represent a rake in this particular order: 
    //   xmin, xmax, ymin, ymax, zmin, zmax
    std::vector<float>  GetRake() const;
    void                SetRake( const std::vector<float>& );

protected:

    static const std::string    _isSteadyTag;
    static const std::string    _velocityMultiplierTag;
    static const std::string    _steadyNumOfStepsTag;
    static const std::string    _seedGenModeTag;
    static const std::string    _seedInputFilenameTag;
    static const std::string    _flowlineOutputFilenameTag;
    static const std::string    _flowDirectionTag;
    static const std::string    _needFlowlineOutputTag;
    static const std::string    _periodicTag;
    static const std::string    _rakeTag;

};

}

#endif
